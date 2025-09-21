import pytest
from unittest.mock import patch, MagicMock
import os

# Set test environment variables to use localhost instead of postgres
os.environ["FLASK_ENV"] = "development"
os.environ["LOCAL_DB_HOST"] = "localhost"
os.environ["LOCAL_DB_PORT"] = "5432"
os.environ["LOCAL_DB_NAME"] = "test_school_api"
os.environ["LOCAL_DB_USER"] = "postgres"
os.environ["LOCAL_DB_PASSWORD"] = "postgres"

# Create a global patcher that starts before imports
mock_pool_patcher = patch("psycopg2.pool.SimpleConnectionPool")
mock_pool = mock_pool_patcher.start()

# Create a mock pool instance
mock_pool_instance = MagicMock()
mock_pool.return_value = mock_pool_instance

# Mock the connection and cursor
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = []
mock_cursor.fetchone.return_value = None
mock_conn.cursor.return_value = mock_cursor

# Mock pool methods
mock_pool_instance.getconn.return_value = mock_conn
mock_pool_instance.putconn.return_value = None

# Now it's safe to import the app
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


# Clean up the patcher when tests are done
def pytest_unconfigure(config):
    mock_pool_patcher.stop()
