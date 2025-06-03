import os
import sys
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import create_engine, MetaData

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


# ---- Get URIs from environment ----
LIVE_DB_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
TEST_DB_URI = os.getenv("SQLALCHEMY_TEST_URI")

if not LIVE_DB_URI or not TEST_DB_URI:
    print("❌ Error: Environment variables SQLALCHEMY_DATABASE_URI and SQLALCHEMY_TEST_URI must be set.")
    sys.exit(1)

# ---- Parse test DB name from URI ----
parsed_test_uri = urlparse(TEST_DB_URI)
TEST_DB_NAME = parsed_test_uri.path.lstrip("/")
POSTGRES_DB_URI = TEST_DB_URI.replace(TEST_DB_NAME, "postgres")  # fallback to create db from 'postgres'

# ---- STEP 1: Create test DB if it doesn't exist ----
def create_test_db():
    try:
        conn = psycopg2.connect(POSTGRES_DB_URI)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            print(f"📀 Creating test database '{TEST_DB_NAME}'...")
            cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
        else:
            print(f"✅ Test database '{TEST_DB_NAME}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating test database:", e)
        sys.exit(1)

# ---- STEP 2: Clone schema from live to test DB ----
def clone_schema():
    try:
        live_engine = create_engine(LIVE_DB_URI)
        test_engine = create_engine(TEST_DB_URI)

        metadata = MetaData()
        metadata.reflect(bind=live_engine)  # Reflect live DB schema
        metadata.create_all(bind=test_engine)  # Create in test DB
        print("✅ Schema copied from live DB to test DB.")
    except Exception as e:
        print("❌ Error copying schema:", e)
        sys.exit(1)

# ---- MAIN ----
if __name__ == "__main__":
    create_test_db()
    clone_schema()