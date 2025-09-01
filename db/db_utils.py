"""
Database compatibility utilities for handling differences between SQLite and PostgreSQL
"""

import os


def get_db_type():
    """Get the current database type from environment variable"""
    return os.getenv("DATABASE_TYPE", "sqlite").lower()


def is_postgresql():
    """Check if we're using PostgreSQL"""
    return get_db_type() == "postgresql"


def get_boolean_true():
    """Get the boolean TRUE value for the current database"""
    return "TRUE" if is_postgresql() else "1"


def get_boolean_false():
    """Get the boolean FALSE value for the current database"""
    return "FALSE" if is_postgresql() else "0"


def get_insert_returning_query(table, columns, returning_column="id"):
    """
    Get an INSERT query with RETURNING clause for PostgreSQL or regular INSERT for SQLite

    Args:
        table (str): Table name
        columns (list): List of column names
        returning_column (str): Column to return (default: id)

    Returns:
        str: The appropriate INSERT query
    """
    placeholders = ", ".join("?" for _ in columns)
    column_names = ", ".join(columns)

    base_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

    if is_postgresql():
        return f"{base_query} RETURNING {returning_column};"
    else:
        return f"{base_query};"


def handle_insert_result(result, cursor=None):
    """
    Handle the result of an INSERT operation for both database types

    Args:
        result: Query result (for PostgreSQL with RETURNING)
        cursor: Database cursor (for SQLite lastrowid)

    Returns:
        int or None: The inserted record ID
    """
    if is_postgresql():
        return result[0]["id"] if result else None
    else:
        return cursor.lastrowid if cursor else None


def get_archived_condition(archived_value=False):
    """
    Get the appropriate condition for checking archived status

    Args:
        archived_value (bool): Whether to check for archived (True) or not archived (False)

    Returns:
        str: The condition string
    """
    if is_postgresql():
        return f"is_archived = {str(archived_value).upper()}"
    else:
        return f"is_archived = {1 if archived_value else 0}"
