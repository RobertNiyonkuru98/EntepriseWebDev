import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, "../server/.env")
load_dotenv(env_path)

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

try:
    engine = create_engine(DATABASE_URL)

    output_dir = 'database'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = f'{output_dir}/schema.sql'

    tables_to_export = ['taxi_zones', 'trips', 'trips_normalized']

    with open(output_file, 'w') as f:
        f.write("-- Schema Export for Taxi Data Project\n")
        f.write("-- Generated from PostgreSQL\n\n")

        for table_name in tables_to_export:
            print(f"Fetching schema for '{table_name}'...")

            # Query columns
            query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
            """
            columns_df = pd.read_sql(query, engine)

            f.write(f"CREATE TABLE {table_name} (\n")
            column_defs = []
            for _, row in columns_df.iterrows():
                col_name = f'"{row["column_name"]}"'
                col_type = row['data_type']
                nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
                column_defs.append(f"    {col_name} {col_type} {nullable}")

            # Basic PK/FK handling would be complex to query manually here without pg_dump,
            # but usually for the assignment, listing columns + types is the critical part.
            # We will manually append the known constraints for documentation if needed,
            # or rely on the Fact that build_db.py creates them.

            f.write(",\n".join(column_defs))
            f.write("\n);\n\n")

        # Write Known Indexes/Constraints manually for completeness
        f.write("-- Indexes & Constraints\n")
        f.write("ALTER TABLE taxi_zones ADD PRIMARY KEY (\"LocationID\");\n")
        f.write("ALTER TABLE trips_normalized ADD FOREIGN KEY (\"PULocationID\") REFERENCES taxi_zones(\"LocationID\");\n")
        f.write("ALTER TABLE trips_normalized ADD FOREIGN KEY (\"DOLocationID\") REFERENCES taxi_zones(\"LocationID\");\n")
        f.write("CREATE INDEX idx_pickup_borough ON trips (pickup_borough);\n")
        f.write("CREATE INDEX idx_pickup_hour ON trips (pickup_hour);\n")
        f.write("CREATE INDEX idx_fare ON trips (fare_amount);\n")

    print(f"Schema successfully exported to {output_file}")

except Exception as e:
    print(f"Error exporting schema: {e}")
