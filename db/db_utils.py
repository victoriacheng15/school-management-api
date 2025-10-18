# PostgreSQL boolean constants
BOOLEAN_TRUE = "TRUE"


def get_insert_returning_query(table, columns, returning_column="id"):
    """
    Get an INSERT query with RETURNING clause for PostgreSQL
    """
    placeholders = ", ".join("%s" for _ in columns)
    column_names = ", ".join(columns)
    base_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    return f"{base_query} RETURNING {returning_column};"


def handle_insert_result(result):
    """
    Handle the result of an INSERT operation for PostgreSQL
    """
    return result[0]["id"] if result else None


def get_archived_condition(archived_value=False):
    """
    Get the appropriate condition for checking archived status (PostgreSQL only)
    """
    return f"is_archived = {str(archived_value).upper()}"
