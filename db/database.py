import psycopg2
import psycopg2.extras
import logging
import os
from dotenv import load_dotenv

# Ensure environment variables from .env are loaded as early as possible so
# Database() instances pick them up no matter the import order elsewhere in
# the application or in tests.
load_dotenv()

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
        Initialize the Database class for PostgreSQL.
        Automatically switches between local and Azure database based on FLASK_ENV.
        """
        flask_env = os.getenv("FLASK_ENV", "development")

        if flask_env == "production":
            # Azure Database configuration - require all environment variables
            required_vars = [
                "AZURE_PG_HOST",
                "AZURE_PG_NAME",
                "AZURE_PG_USER",
                "AZURE_PG_PASSWORD",
            ]
            missing_vars = [var for var in required_vars if not os.getenv(var)]

            if missing_vars:
                error_msg = f"Missing required Azure database environment variables: {', '.join(missing_vars)}"
                error_msg += "\nPlease set these variables in your .env file for production environment."
                logger.error(error_msg)
                raise ValueError(error_msg)

            self.db_config = {
                "host": os.getenv("AZURE_PG_HOST"),
                "port": os.getenv("AZURE_PG_PORT", "5432"),
                "database": os.getenv("AZURE_PG_NAME"),
                "user": os.getenv("AZURE_PG_USER"),
                "password": os.getenv("AZURE_PG_PASSWORD"),
            }

            logger.info("Using Azure Database for PostgreSQL (production)")
        else:
            # Local Database configuration (development) - require all environment variables
            required_vars = [
                "LOCAL_DB_HOST",
                "LOCAL_DB_NAME",
                "LOCAL_DB_USER",
                "LOCAL_DB_PASSWORD",
            ]
            missing_vars = [var for var in required_vars if not os.getenv(var)]

            if missing_vars:
                error_msg = f"Missing required local database environment variables: {', '.join(missing_vars)}"
                error_msg += "\nPlease set these variables in your .env file for development environment."
                logger.error(error_msg)
                raise ValueError(error_msg)

            self.db_config = {
                "host": os.getenv("LOCAL_DB_HOST"),
                "port": os.getenv("LOCAL_DB_PORT", "5432"),
                "database": os.getenv("LOCAL_DB_NAME"),
                "user": os.getenv("LOCAL_DB_USER"),
                "password": os.getenv("LOCAL_DB_PASSWORD"),
            }
            logger.info("Using Local Database (development)")
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the PostgreSQL database.
        """
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(**self.db_config)
                self.cursor = self.conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                logger.info(
                    f"Successfully connected to PostgreSQL database: {self.db_config['database']}"
                )
            except psycopg2.Error as e:
                logger.error(f"Error connecting to database: {e}")
                raise

    def close(self):
        """
        Close the connection to the PostgreSQL database.
        """
        if self.conn:
            try:
                self.conn.commit()
                self.conn.close()
                logger.info(f"Connection to {self.db_config['database']} closed.")
            except psycopg2.Error as e:
                logger.error(f"Error closing the connection: {e}")
            finally:
                self.conn = None
                self.cursor = None

    def execute_query(self, query, params=()):
        """
        Execute a single SQL query (PostgreSQL only).
        """
        self.connect()
        try:
            if "?" in query:
                query = query.replace("?", "%s")
            self.cursor.execute(query, params)
            logger.info(f"Executed query: {query}")
            if (
                query.strip().lower().startswith("select")
                or "returning" in query.lower()
            ):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor
        except psycopg2.IntegrityError as e:
            logger.warning(f"Integrity error: {e}")
            raise ValueError(f"Integrity error: {str(e)}")
        except psycopg2.Error as e:
            logger.error(f"Error executing query: {e}")
            raise RuntimeError(f"Database error: {str(e)}")
        finally:
            self.close()

    def execute_many(self, query, param_list):
        """
        Execute a query with multiple sets of parameters (bulk insert, PostgreSQL only).
        """
        self.connect()
        try:
            if "?" in query:
                query = query.replace("?", "%s")
            self.cursor.executemany(query, param_list)
            self.conn.commit()
            logger.info(f"Executed many: {query}")
            return self.cursor
        except psycopg2.Error as e:
            logger.error(f"Error executing many: {e}")
            return None
        finally:
            self.close()

    def execute_script(self, script):
        """
        Execute multiple SQL commands from a script (PostgreSQL only).
        """
        self.connect()
        try:
            statements = [stmt.strip() for stmt in script.split(";") if stmt.strip()]
            for statement in statements:
                if statement:
                    self.cursor.execute(statement)
            self.conn.commit()
            logger.info(f"Executed script with multiple SQL commands.")
        except psycopg2.Error as e:
            logger.error(f"Error executing script: {e}")
        finally:
            self.close()

    def get_last_insert_id(self):
        """
        Get the ID of the last inserted row (PostgreSQL only).
        """
        return (
            self.cursor.fetchone()[0]
            if self.cursor and self.cursor.description
            else None
        )
