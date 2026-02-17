import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
print("Connecting to Nuke DB...", flush=True)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    print("Dropping Schema public (Cascading)...", flush=True)
    cur.execute("DROP SCHEMA public CASCADE;")
    print("Schema dropped.", flush=True)

    print("Recreating Schema public...", flush=True)
    cur.execute("CREATE SCHEMA public;")
    print("Schema recreated. Database is empty and fresh.", flush=True)

    conn.close()
except Exception as e:
    print(f"Error nuking DB: {e}", flush=True)
