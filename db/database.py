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
        Initialize the Database class for PostgreSQL only.
        """
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "school"),
            "user": os.getenv("DB_USER", "schooluser"),
            "password": os.getenv("DB_PASSWORD", "schoolpass"),
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the PostgreSQL database.
        """
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(**self.db_config)
                self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                logger.info(f"Successfully connected to PostgreSQL database: {self.db_config['database']}")
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
            if query.strip().lower().startswith("select") or "returning" in query.lower():
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
        return self.cursor.fetchone()[0] if self.cursor and self.cursor.description else None
