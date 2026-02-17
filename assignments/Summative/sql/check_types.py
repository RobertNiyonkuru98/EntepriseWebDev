import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)

query = """
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'trips';
"""

df = pd.read_sql(query, engine)
print(f"{'Column':<25} | {'Type':<15}")
print("-" * 45)
for index, row in df.iterrows():
    print(f"{row['column_name']:<25} | {row['data_type']:<15}")
