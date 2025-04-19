import sqlite3
import os
import logging


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO, 
    handlers=[
        logging.StreamHandler()
        # Optionally, you can log to a file by adding a file handler
        # logging.FileHandler('db_init.log')  # Uncomment to log to a file
    ]
)

logger = logging.getLogger(__name__)

def check_db_exists(db_path):
    """
    Checks if the SQLite database file exists in the 'db' directory.

    Args:
        db_path (str): Path to the database file.

    Returns:
        bool: True if the database file exists, False otherwise.
    """
    return os.path.exists(db_path)

def read_schema_file():
    """
    Attempts to read the 'schema.sql' file from the 'db' directory.
    
    If the file is found, it returns the contents as a string. 
    If the file is not found, it logs an error and returns None.

    Returns:
        str: The contents of the schema file, or None if the file is not found.
    """
    schema_path = os.path.join("db", "schema.sql")

    try:
        with open(schema_path, "r") as schema_file:
            schema_sql = schema_file.read()
        return schema_sql
    except FileNotFoundError:
        logger.error(f"Schema file {schema_path} not found.")
        return None


def init_db():
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
    db_path = os.path.join("db", "school.db")

    # If the database already exists, log the message and skip initialization
    if check_db_exists(db_path):
        logger.info(f"Database {db_path} already exists. Skipping initialization.")
        return

    # Read the schema from the schema.sql file
    schema_sql = read_schema_file()
    if schema_sql is None:
        logger.error("Initialization aborted due to missing schema file.")
        return

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.executescript(schema_sql)

        connection.commit()
        connection.close()

        logger.info(f"Database {db_path} initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")


if __name__ == "__main__":
    init_db()
