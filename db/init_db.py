import os
import logging
import sqlite3
from database import Database


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
        # Optionally, you can log to a file by adding a file handler
        # logging.FileHandler('db_init.log')  # Uncomment to log to a file
    ],
)

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = os.path.join("db", "school.db")
DEFAULT_SCHEMA_PATH = os.path.join("db", "schema.sql")


def read_schema_file(schema_path=DEFAULT_SCHEMA_PATH):
    """Read the schema file containing SQL commands to initialize the database."""
    try:
        with open(schema_path, "r") as file:
            schema_sql = file.read()
        return schema_sql
    except FileNotFoundError:
        logger.error(f"Schema file {schema_path} not found.")
        return None


def init_db(db_path=DEFAULT_DB_PATH, schema_path=DEFAULT_SCHEMA_PATH):
    """
    Initializes the SQLite database by creating the database file and
    executing the schema defined in the 'schema.sql' file.

    Steps:
    1. Checks if the database file already exists in the 'db' directory.
    2. If the database file exists, logs a message and skips initialization.
    3. If the database does not exist:
        - Reads the SQL schema from the 'schema.sql' file.
        - Creates a connection to the SQLite database and executes the schema.
        - Commits the transaction and closes the connection.
    4. Logs success or failure during the initialization process.

    Returns:
        None

    Raises:
        sqlite3.Error: If an error occurs while initializing the SQLite database.
    """
    # If the database already exists, log the message and skip initialization
    if os.path.exists(DEFAULT_DB_PATH):
        logger.info(
            f"Database {DEFAULT_DB_PATH} already exists. Skipping initialization."
        )
        return

    # Read the schema from the schema.sql file
    schema_sql = read_schema_file(schema_path)
    if schema_sql is None:
        logger.error("Initialization aborted due to missing schema file.")
        return

    try:
        db = Database()
        db.connect()
        db.execute_script(schema_sql)
        db.close()

        logger.info(f"Database {db_path} initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")


if __name__ == "__main__":
    init_db()
