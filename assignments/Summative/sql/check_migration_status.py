import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

try:
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM trips;")
    count = cur.fetchone()[0]
    print(f"Current row count in 'trips': {count}")
    conn.close()
except Exception as e:
    print(f"Error checking count: {e}")
