import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Float, Text, BigInteger
import io
from dotenv import load_dotenv
import os

# Load environment variables (Relative path fix)
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, "../server/.env")
load_dotenv(env_path)

# Database Connection
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Data Paths (Relative path fix)
parquet_file = os.path.join(script_dir, "../ETL/assets/integrated_taxi_data.parquet")
zone_csv_path = os.path.join(script_dir, "../ETL/assets/taxi_zone_lookup.csv")

print("Starting optimized database migration to PostgreSQL...")
print(f"Reading {parquet_file}...")
# Use 100k rows for faster iteration, user can change this to 500k-1M for production
df = pd.read_parquet(parquet_file).head(100000)

# Ensure datetime columns are strings/objects for CSV conversion
df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].astype(str)
df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].astype(str)

print(f"Prepared {len(df)} rows.")

# Define explicit dtypes for SQLAlchemy
dtype_mapping = {
    'VendorID': BigInteger,
    'tpep_pickup_datetime': Text,
    'tpep_dropoff_datetime': Text,
    'passenger_count': Integer,
    'trip_distance': Float,
    'RatecodeID': Integer,
    'store_and_fwd_flag': Text,
    'PULocationID': Integer,
    'DOLocationID': Integer,
    'payment_type': Integer,
    'fare_amount': Float,
    'extra': Float,
    'mta_tax': Float,
    'tip_amount': Float,
    'tolls_amount': Float,
    'improvement_surcharge': Float,
    'total_amount': Float,
    'congestion_surcharge': Float,
    'pickup_borough': Text,
    'pickup_zone': Text,
    'dropoff_borough': Text,
    'dropoff_zone': Text,
    'duration_hours': Float,
    'avg_speed_kmh': Float,
    'fare_per_mile': Float,
    'pickup_hour': Integer
}

# --- 1. SETUP ENGINE & LIVE TABLE ---
engine = create_engine(DATABASE_URL)

# Create the table schema for the LIVE app (De-normalized)
# We use head(0) to create just the table structure
print("Creating 'trips' table (Live App)...")
df.head(0).to_sql("trips", engine, if_exists="replace", index=False, dtype=dtype_mapping)

# --- 2. ERD NORMALIZATION SUPPORT ---
print("Creating Normalized Tables for ERD...")

# Create and Populate `taxi_zones`
try:
    zone_df = pd.read_csv(zone_csv_path)
    zone_df.to_sql("taxi_zones", engine, if_exists="replace", index=False, dtype={
        "LocationID": Integer,
        "Borough": Text,
        "Zone": Text,
        "service_zone": Text
    })
    # Add Primary Key to taxi_zones (PostgreSQL specific)
    with engine.connect() as con:
        con.execute(text("ALTER TABLE taxi_zones ADD PRIMARY KEY (\"LocationID\");"))
    print("Table 'taxi_zones' created and populated.")
except Exception as e:
    print(f"Error creating taxi_zones: {e}")

# Create `trips_normalized` structure
print("Creating 'trips_normalized' table...")
df.head(0).to_sql("trips_normalized", engine, if_exists="replace", index=False, dtype=dtype_mapping)

with engine.connect() as con:
    # Add Foreign Key Constraints (This makes the ERD valid)
    try:
        # Note: We must ensure PULocationID/DOLocationID columns exist and match types
        con.execute(text("ALTER TABLE trips_normalized ADD CONSTRAINT fk_pickup FOREIGN KEY (\"PULocationID\") REFERENCES taxi_zones(\"LocationID\");"))
        con.execute(text("ALTER TABLE trips_normalized ADD CONSTRAINT fk_dropoff FOREIGN KEY (\"DOLocationID\") REFERENCES taxi_zones(\"LocationID\");"))
        print("Foreign Keys added to 'trips_normalized'.")
    except Exception as e:
        print(f"Error adding FKs to trips_normalized: {e}")

# --- 3. BULK DATA UPLOAD ---
# Connect using raw psycopg2 for COPY performance
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Prepare CSV buffer
print("Converting dataframe to CSV buffer...")
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False, header=False)
csv_buffer.seek(0)

print("copying data to database using COPY command (this is fast)...")
try:
    # Populate LIVE 'trips' table
    cur.copy_expert("COPY trips FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    print("Data uploaded to 'trips' (Live App).")

    # Populate ERD 'trips_normalized' table
    csv_buffer.seek(0) # Reset buffer to start
    cur.copy_expert("COPY trips_normalized FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    print("Data uploaded to 'trips_normalized' (ERD).")

    conn.commit()
    print("All Data upload complete.")
except Exception as e:
    conn.rollback()
    print(f"Error uploading data: {e}")
    exit(1)

# --- 4. INDEXES ---
print("Creating Indexes for performance...")
try:
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pickup_borough ON trips (pickup_borough);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pickup_hour ON trips (pickup_hour);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fare ON trips (fare_amount);")
    conn.commit()
    print("Indexes created successfully.")
except Exception as e:
    print(f"Error creating indexes: {e}")

cur.close()
conn.close()
print("Migration completed successfully.")