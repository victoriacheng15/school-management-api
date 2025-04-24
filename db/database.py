import sqlite3
import logging
import os

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


class Database:
    def __init__(self):
        """
        Initialize the Database class with the given database name.

        Args:
            db_name (str): The name (or path) of the SQLite database file.
        """
        self.db_name = os.path.join("db", "school.db")
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the SQLite database.

        This method opens a connection to the SQLite database and creates a cursor object.
        """
        if not self.conn:
            try:
                self.conn = sqlite3.connect(self.db_name)
                self.cursor = self.conn.cursor()
                logger.info(f"Successfully connected to the database: {self.db_name}")
            except sqlite3.Error as e:
                logger.error(f"Error connecting to database: {e}")

    def close(self):
        """
        Close the connection to the database.

        If the connection is open, it will commit any changes and close the connection.
        """
        if self.conn:
            try:
                self.conn.commit()
                self.conn.close()
                logger.info(f"Connection to {self.db_name} closed.")
            except sqlite3.Error as e:
                logger.error(f"Error closing the connection: {e}")

    def execute_query(self, query, params=()):
        """
        Execute a single SQL query.

        Args:
            query (str): The SQL query string to execute.
            params (tuple): The parameters to pass to the query (optional).

        Returns:
            list: A list of results if the query returns data.
        """
        self.connect()
        try:
            self.cursor.execute(query, params)
            logger.info(f"Executed query: {query}")
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            return None
        finally:
            self.close()

    def execute_many(self, query, param_list):
        """
        Execute a query with multiple sets of parameters (bulk insert).

        Args:
            query (str): The SQL query string with placeholders.
            param_list (list of tuples): Each tuple contains the parameters for one row.
        """
        self.connect()
        try:
            self.cursor.executemany(query, param_list)
            logger.info(f"Executed many: {query}")
        except sqlite3.Error as e:
            logger.error(f"Error executing many: {e}")

    def execute_script(self, script):
        """
        Execute multiple SQL commands from a script.

        Args:
            script (str): The SQL script containing multiple SQL commands to execute.
        """
        self.connect()
        try:
            self.cursor.executescript(script)
            logger.info(f"Executed script with multiple SQL commands.")
        except sqlite3.Error as e:
            logger.error(f"Error executing script: {e}")
        finally:
            self.close()
