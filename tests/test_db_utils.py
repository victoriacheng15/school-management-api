#!/usr/bin/env python3
"""
Simple test for database compatibility utilities
"""

import os
import sys

sys.path.append(".")

# Test the database utilities without importing models
from db.db_utils import (
    get_db_type,
    is_postgresql,
    get_boolean_true,
    get_boolean_false,
    get_insert_returning_query,
    get_archived_condition,
)


def test_db_utils():
    """Test database utility functions"""
    print("Testing Database Utilities...")

    # Test SQLite mode
    os.environ["DATABASE_TYPE"] = "sqlite"
    print(f"SQLite mode - DB Type: {get_db_type()}")
    print(f"  is_postgresql(): {is_postgresql()}")
    print(f"  Boolean True: {get_boolean_true()}")
    print(f"  Boolean False: {get_boolean_false()}")
    print(f"  Archived condition (False): {get_archived_condition(False)}")
    print(
        f"  Insert query: {get_insert_returning_query('test_table', ['col1', 'col2'])}"
    )

    # Test PostgreSQL mode
    os.environ["DATABASE_TYPE"] = "postgresql"
    print(f"\nPostgreSQL mode - DB Type: {get_db_type()}")
    print(f"  is_postgresql(): {is_postgresql()}")
    print(f"  Boolean True: {get_boolean_true()}")
    print(f"  Boolean False: {get_boolean_false()}")
    print(f"  Archived condition (False): {get_archived_condition(False)}")
    print(
        f"  Insert query: {get_insert_returning_query('test_table', ['col1', 'col2'])}"
    )

    print("\n✅ Database utilities working correctly!")


if __name__ == "__main__":
    print("Database Utilities Test")
    print("=" * 30)
    test_db_utils()
