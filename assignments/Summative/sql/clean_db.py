import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../server/.env")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Connecting to: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("Dropping 'trips' table to free space...")
    cur.execute("DROP TABLE IF EXISTS trips cascade;")
    conn.commit()
    print("Table dropped successfully.")

    # Run a vacuum to reclaim space immediately if possible
    # ( VACUUM FULL cannot run inside a transaction block usually, so we set autocommit)
    conn.set_session(autocommit=True)
    print("Running VACUUM to reclaim storage...")
    try:
        cur.execute("VACUUM FULL;")
        print("VACUUM completed.")
    except Exception as e:
        print(f"VACUUM failed (might not be necessary/allowed): {e}")

    conn.close()
except Exception as e:
    print(f"Error cleaning DB: {e}")
