import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Connecting to terminate queries...", flush=True)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # Terminate other sessions that might be holding locks
    print("Terminating active queries...", flush=True)
    cur.execute("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE pid <> pg_backend_pid()
          AND state IN ('active', 'idle in transaction')
          AND datname = current_database();
    """)
    print("Queries terminated.", flush=True)

    conn.close()
except Exception as e:
    print(f"Error terminating queries: {e}", flush=True)
