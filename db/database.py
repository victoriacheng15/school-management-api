import psycopg2
import psycopg2.extras
from psycopg2 import pool
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


def _check_required_env_vars(vars_list, env_type):
    """Helper function to check required environment variables."""
    missing_vars = [var for var in vars_list if not os.getenv(var)]
    if missing_vars:
        error_msg = f"Missing required {env_type} database environment variables: {', '.join(missing_vars)}"
        error_msg += f"\nPlease set these variables in your .env file for {env_type} environment."
        logger.error(error_msg)
        raise ValueError(error_msg)


def _is_production():
    """Check if running in production environment."""
    return os.getenv("FLASK_ENV", "development") == "production"


class Database:
    # Class-level flags to track if we've already logged the database type
    _logged_azure = False
    _logged_local = False
    _pool = None  # Connection pool
    _db_config = None  # Store config for pool creation

    def __init__(self):
        """
        Initialize the Database class for PostgreSQL with connection pooling.
        Automatically switches between local and Azure database based on FLASK_ENV.
        """
        # Only create config and pool once
        if Database._db_config is None:
            if _is_production():
                # Azure Database configuration
                required_vars = [
                    "AZURE_PG_HOST",
                    "AZURE_PG_NAME",
                    "AZURE_PG_USER",
                    "AZURE_PG_PASSWORD",
                ]
                _check_required_env_vars(required_vars, "Azure")

                Database._db_config = {
                    "host": os.getenv("AZURE_PG_HOST"),
                    "port": os.getenv("AZURE_PG_PORT", "5432"),
                    "database": os.getenv("AZURE_PG_NAME"),
                    "user": os.getenv("AZURE_PG_USER"),
                    "password": os.getenv("AZURE_PG_PASSWORD"),
                    "sslmode": os.getenv("AZURE_PG_SSLMODE", "require"),
                }

                # Only log once per application lifecycle
                if not Database._logged_azure:
                    logger.info("Using Azure Database for PostgreSQL (production)")
                    Database._logged_azure = True
            else:
                # Local Database configuration
                required_vars = [
                    "LOCAL_DB_HOST",
                    "LOCAL_DB_NAME",
                    "LOCAL_DB_USER",
                    "LOCAL_DB_PASSWORD",
                ]
                _check_required_env_vars(required_vars, "local")

                Database._db_config = {
                    "host": os.getenv("LOCAL_DB_HOST"),
                    "port": os.getenv("LOCAL_DB_PORT", "5432"),
                    "database": os.getenv("LOCAL_DB_NAME"),
                    "user": os.getenv("LOCAL_DB_USER"),
                    "password": os.getenv("LOCAL_DB_PASSWORD"),
                }

                # Only log once per application lifecycle
                if not Database._logged_local:
                    logger.info("Using Local Database (development)")
                    Database._logged_local = True

            # Create connection pool once
            try:
                Database._pool = pool.SimpleConnectionPool(
                    1,  # minimum connections
                    3,  # maximum connections (reduced for memory constraints)
                    **Database._db_config,
                )
                logger.info("Database connection pool created (1-3 connections)")
            except Exception as e:
                logger.error(f"Failed to create connection pool: {e}")
                raise

        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Get a connection from the connection pool.
        """
        if self.conn is None:
            try:
                self.conn = Database._pool.getconn()
                self.cursor = self.conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                # Reduce connection logging in production to minimize log volume
                if not _is_production():
                    logger.info(
                        f"Successfully connected to PostgreSQL database: {Database._db_config['database']}"
                    )
            except psycopg2.Error as e:
                logger.error(f"Error connecting to database: {e}")
                raise

    def close(self):
        """
        Return the connection to the pool.
        """
        if self.conn:
            try:
                self.conn.commit()
                if self.cursor:
                    self.cursor.close()
                # Return connection to pool instead of closing
                Database._pool.putconn(self.conn)
                # Reduce connection logging in production to minimize log volume
                if not _is_production():
                    logger.info(f"Connection returned to pool.")
            except psycopg2.Error as e:
                logger.error(f"Error returning connection to pool: {e}")
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

            # Only log queries in development to reduce log volume in production
            if not _is_production():
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

            # Only log in development to reduce log volume in production
            if not _is_production():
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

            # Only log in development to reduce log volume in production
            if not _is_production():
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
