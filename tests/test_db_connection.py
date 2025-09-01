#!/usr/bin/env python3
"""
Test script to verify database connections work for both SQLite and PostgreSQL
"""

import os
import sys

sys.path.append(".")

from db.database import Database


def test_sqlite():
    print("Testing SQLite connection...")
    os.environ["DATABASE_TYPE"] = "sqlite"

    try:
        db = Database()
        result = db.execute_query("SELECT 1 as test")
        print(f"✅ SQLite connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False


def test_postgresql():
    print("Testing PostgreSQL connection...")
    os.environ["DATABASE_TYPE"] = "postgresql"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "school"
    os.environ["DB_USER"] = "schooluser"
    os.environ["DB_PASSWORD"] = "schoolpass"

    try:
        db = Database()
        result = db.execute_query("SELECT 1 as test")
        print(f"✅ PostgreSQL connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


if __name__ == "__main__":
    print("Database Connection Test")
    print("=" * 40)

    sqlite_ok = test_sqlite()
    postgresql_ok = test_postgresql()

    print("\nSummary:")
    print(f"SQLite: {'✅ Working' if sqlite_ok else '❌ Failed'}")
    print(f"PostgreSQL: {'✅ Working' if postgresql_ok else '❌ Failed'}")

    if sqlite_ok and postgresql_ok:
        print("\n🎉 Both database connections are working!")
        sys.exit(0)
    else:
        print("\n⚠️  Some database connections failed")
        sys.exit(1)
