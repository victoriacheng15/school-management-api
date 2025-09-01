import sqlite3
import psycopg2
import psycopg2.extras
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
        Initialize the Database class with support for both SQLite and PostgreSQL.
        Database type is determined by the DATABASE_TYPE environment variable.
        """
        self.db_type = os.getenv("DATABASE_TYPE", "sqlite").lower()
        self.conn = None
        self.cursor = None

        if self.db_type == "postgresql":
            self.db_config = {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": os.getenv("DB_PORT", "5432"),
                "database": os.getenv("DB_NAME", "school"),
                "user": os.getenv("DB_USER", "schooluser"),
                "password": os.getenv("DB_PASSWORD", "schoolpass"),
            }
        else:
            self.db_name = os.path.join("db", "school.db")

    def connect(self):
        """
        Connect to the database (SQLite or PostgreSQL).

        This method opens a connection to the database and creates a cursor object.
        """
        if self.conn is None:
            try:
                if self.db_type == "postgresql":
                    self.conn = psycopg2.connect(**self.db_config)
                    self.cursor = self.conn.cursor(
                        cursor_factory=psycopg2.extras.RealDictCursor
                    )
                    logger.info(
                        f"Successfully connected to PostgreSQL database: {self.db_config['database']}"
                    )
                else:
                    self.conn = sqlite3.connect(self.db_name)
                    self.conn.row_factory = sqlite3.Row  # Enable dict-like access
                    self.cursor = self.conn.cursor()
                    logger.info(
                        f"Successfully connected to SQLite database: {self.db_name}"
                    )
            except (sqlite3.Error, psycopg2.Error) as e:
                logger.error(f"Error connecting to database: {e}")
                raise

    def close(self):
        """
        Close the connection to the database.

        If the connection is open, it will commit any changes and close the connection.
        """
        if self.conn:
            try:
                self.conn.commit()
                self.conn.close()
                db_name = (
                    self.db_config["database"]
                    if self.db_type == "postgresql"
                    else self.db_name
                )
                logger.info(f"Connection to {db_name} closed.")
            except (sqlite3.Error, psycopg2.Error) as e:
                logger.error(f"Error closing the connection: {e}")
            finally:
                self.conn = None
                self.cursor = None

    def execute_query(self, query, params=()):
        """
        Execute a single SQL query.

        Args:
            query (str): The SQL query string to execute.
            params (tuple): The parameters to pass to the query (optional).

        Returns:
            list: A list of results if the query returns data, or the cursor for non-SELECT queries.
        """
        self.connect()
        try:
            # Convert SQLite-style parameters (?) to PostgreSQL-style (%s) if needed
            if self.db_type == "postgresql" and "?" in query:
                query = query.replace("?", "%s")

            self.cursor.execute(query, params)
            logger.info(f"Executed query: {query}")
            if query.strip().lower().startswith("select") or "returning" in query.lower():
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor
        except (sqlite3.IntegrityError, psycopg2.IntegrityError) as e:
            logger.warning(f"Integrity error: {e}")
            raise ValueError(f"Integrity error: {str(e)}")
        except (sqlite3.Error, psycopg2.Error) as e:
            logger.error(f"Error executing query: {e}")
            raise RuntimeError(f"Database error: {str(e)}")
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
            # Convert SQLite-style parameters (?) to PostgreSQL-style (%s) if needed
            if self.db_type == "postgresql" and "?" in query:
                query = query.replace("?", "%s")

            self.cursor.executemany(query, param_list)
            self.conn.commit()
            logger.info(f"Executed many: {query}")
            return self.cursor
        except (sqlite3.Error, psycopg2.Error) as e:
            logger.error(f"Error executing many: {e}")
            return None
        finally:
            self.close()

    def execute_script(self, script):
        """
        Execute multiple SQL commands from a script.

        Args:
            script (str): The SQL script containing multiple SQL commands to execute.
        """
        self.connect()
        try:
            if self.db_type == "postgresql":
                # PostgreSQL doesn't have executescript, so split and execute individually
                statements = [
                    stmt.strip() for stmt in script.split(";") if stmt.strip()
                ]
                for statement in statements:
                    if statement:
                        self.cursor.execute(statement)
                self.conn.commit()
            else:
                self.cursor.executescript(script)
            logger.info(f"Executed script with multiple SQL commands.")
        except (sqlite3.Error, psycopg2.Error) as e:
            logger.error(f"Error executing script: {e}")
        finally:
            self.close()

    def get_last_insert_id(self):
        """
        Get the ID of the last inserted row.

        Returns:
            int: The last inserted row ID
        """
        if self.db_type == "postgresql":
            # PostgreSQL uses RETURNING clause or currval()
            # This method should be called after an INSERT with RETURNING id
            return self.cursor.fetchone()[0] if self.cursor.description else None
        else:
            # SQLite uses lastrowid
            return self.cursor.lastrowid if self.cursor else None
