import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("AZURE_PG_HOST"),
    "port": os.getenv("AZURE_PG_PORT"),
    "database": os.getenv("AZURE_PG_NAME"),
    "user": os.getenv("AZURE_PG_USER"),
    "password": os.getenv("AZURE_PG_PASSWORD"),
    "sslmode": "require",
}

def drop_all_tables():
    print("Connecting to Azure PostgreSQL DB...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    print("Fetching all tables in public schema...")
    cur.execute("""
        SELECT tablename FROM pg_tables WHERE schemaname = 'public';
    """)
    tables = [row[0] for row in cur.fetchall()]
    if not tables:
        print("No tables found.")
        return
    print(f"Dropping tables: {tables}")
    for table in tables:
        print(f"Dropping table: {table}")
        cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
    cur.close()
    conn.close()
    print("✅ All tables dropped.")

if __name__ == "__main__":
    drop_all_tables()
