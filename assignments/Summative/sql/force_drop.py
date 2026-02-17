import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Connecting to DB...", flush=True)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    print("Dropping 'trips' table...", flush=True)
    cur.execute("DROP TABLE IF EXISTS trips CASCADE;")
    print("Table dropped.", flush=True)

    conn.close()
except Exception as e:
    print(f"Error dropping table: {e}", flush=True)
