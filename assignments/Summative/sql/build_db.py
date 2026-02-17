import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Float, Text, BigInteger
import io
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("../server/.env")

# Database Connection
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

parquet_file = "../ETL/assets/integrated_taxi_data.parquet"

print("Starting optimized database migration to PostgreSQL...")
print(f"Reading {parquet_file}...")
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

# Create the table schema using SQLAlchemy (but not inserting data)
engine = create_engine(DATABASE_URL)
# We use head(0) to create just the table structure
df.head(0).to_sql("trips", engine, if_exists="replace", index=False, dtype=dtype_mapping)
print("Table 'trips' created/replaced with optimized schema.")

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
    cur.copy_expert("COPY trips FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    conn.commit()
    print("Data upload complete.")
except Exception as e:
    conn.rollback()
    print(f"Error uploading data: {e}")
    exit(1)

# Create Indexes
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