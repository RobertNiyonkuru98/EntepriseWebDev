from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Testing connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Connection successful!")
        conn.execute(text("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY);"))
        print("Table creation successful!")
        conn.commit()
except Exception as e:
    print("Connection failed!")
    print(e)
