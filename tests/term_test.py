import pytest
import os
from datetime import date
from unittest.mock import patch
from app.models import (
    term_db_read_all,
    term_db_read_by_id,
    term_db_read_by_ids,
    term_db_insert,
    term_db_update,
    term_db_archive,
)
from app.services import (
    get_all_terms,
    get_term_by_id,
    create_new_terms,
    update_terms,
    archive_terms,
)

# =======================
# Fixtures
# =======================


def make_term_row():
    today = date.today().isoformat()
    return {
        "id": 1,
        "name": "Fall 2025",
        "start_date": "2025-09-01",
        "end_date": "2025-12-15",
        "created_at": today,
        "updated_at": today,
    }


def make_term_dict():
    return {
        "name": "Fall 2025",
        "start_date": "2025-09-01",
        "end_date": "2025-12-15",
    }


@pytest.fixture
def valid_term_row():
    return make_term_row()


@pytest.fixture
def valid_term_rows():
    return [make_term_row() for _ in range(2)]


@pytest.fixture
def valid_term_create_data():
    return [
        make_term_dict(),
        {
            "name": "Winter 2026",
            "start_date": "2026-01-06",
            "end_date": "2026-04-20",
        },
    ]


@pytest.fixture
def valid_term_update_data():
    data = make_term_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def term_missing_id(valid_term_update_data):
    data = [item.copy() for item in valid_term_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_term_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.term.term_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.term.term_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.term.term_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.term.term_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.term.term_db_update") as mock:
        yield mock


@pytest.fixture
def valid_term_ids():
    return [1, 2]


@pytest.fixture
def mock_db_archive():
    with patch("app.services.term.term_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestTermReadService:
    def test_get_all_terms(self, mock_db_read_all, valid_term_row):
        # Service layer expects dicts since model layer converts tuples to dicts
        mock_db_read_all.return_value = [valid_term_row]

        terms = get_all_terms(active_only=True)

        assert len(terms) == 1
        assert terms[0]["name"] == "Fall 2025"
        mock_db_read_all.assert_called_once()

    def test_get_all_terms_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_terms(active_only=True)

    def test_get_term_by_id(self, mock_db_read_one, valid_term_row):
        # Service layer expects dicts since model layer converts tuples to dicts
        mock_db_read_one.return_value = valid_term_row

        term = get_term_by_id(1)
        assert term["name"] == "Fall 2025"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_term_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        term = get_term_by_id(123)
        assert term is None


@patch("app.models.term.db")
@patch("app.services.term.term_dict_to_row")
class TestTermCreateService:
    def test_create_new_terms(
        self,
        mock_term_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_term_create_data,
        valid_term_rows,
    ):
        # Mock the converter function
        mock_term_dict_to_row.side_effect = lambda d: tuple(d.values())

        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"lastrowid": None}
        )()

        # For PostgreSQL, insert returns IDs via RETURNING; for SQLite, returns lastrowid
        mock_db_create.side_effect = [1, 2]

        # Handle PostgreSQL format for read_many
        mock_db_read_many.return_value = valid_term_rows

        results, error, status_code = create_new_terms(valid_term_create_data)

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_terms_failure(
        self,
        mock_term_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_term_create_data,
    ):
        # Mock the converter function
        mock_term_dict_to_row.side_effect = lambda d: tuple(d.values())

        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"lastrowid": None}
        )()

        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_terms(valid_term_create_data)

        assert results == []
        assert error["message"] == "No terms were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


@patch("app.models.term.db")
@patch("app.services.term.term_dict_to_row")
class TestTermUpdateService:
    def test_update_terms(
        self,
        mock_term_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_term_update_data,
        valid_term_row,
    ):
        # Mock the converter function
        mock_term_dict_to_row.side_effect = lambda d: tuple(d.values())

        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 1}
        )()

        mock_db_update.return_value = 1

        # Handle PostgreSQL format for read_one (used by bulk operations)
        mock_db_read_one.return_value = valid_term_row
        mock_db_read_many.return_value = [valid_term_row]

        results, error, status_code = update_terms(valid_term_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_terms_no_success(
        self,
        mock_term_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_term_update_data,
    ):
        # Mock the converter function
        mock_term_dict_to_row.side_effect = lambda d: tuple(d.values())

        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 0}
        )()

        # Mock existing record lookup (bulk operations check if record exists first)
        mock_db_read_one.return_value = {"id": 1}  # Record exists

        mock_db_update.return_value = 0
        results, error, status_code = update_terms(valid_term_update_data)

        assert results == []
        assert error == [{"message": "Term ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_terms_missing_id(
        self,
        mock_term_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        term_missing_id,
    ):
        # Mock the converter function
        mock_term_dict_to_row.side_effect = lambda d: tuple(d.values())

        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 0}
        )()

        results, error, status_code = update_terms(term_missing_id)

        assert results == []
        assert error == [{"message": "Missing term ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


@patch("app.models.term.db")
class TestTermArchiveService:
    def test_archive_terms(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_term_ids,
    ):
        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 1}
        )()

        # Mock existing record lookup (bulk operations check if record exists first)
        mock_db_read_one.return_value = {"id": 1}  # Record exists

        # Mock reading archived records at the end
        mock_db_read_many.return_value = [{"id": 1}, {"id": 2}]

        mock_db_archive.side_effect = [1, 1]
        archived, errors, status_code = archive_terms(valid_term_ids)

        assert len(archived) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_terms_none_archived(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_term_ids,
    ):
        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 0}
        )()

        # Mock existing record lookup (bulk operations check if record exists first)
        mock_db_read_one.return_value = {"id": 1}  # Record exists

        # Mock reading archived records at the end (empty since none archived)
        mock_db_read_many.return_value = []

        mock_db_archive.return_value = 0
        archived, errors, status_code = archive_terms(valid_term_ids)

        assert archived == []

    def test_archive_terms_invalid_ids(self, mock_db_instance):
        # Mock database instance methods
        mock_db_instance.execute_query.return_value = type(
            "MockCursor", (), {"rowcount": 0}
        )()

        results, errors, status = archive_terms(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestTermModel:
    @patch("app.models.term.db.execute_query")
    def test_term_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": "data"}]
        result = term_db_read_all()
        assert result == [{"mocked": "data"}]
        mock_execute.assert_called_once_with("SELECT * FROM terms;")

    @patch("app.models.term.db.execute_query")
    def test_term_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"id": 1, "name": "term_1"}]
        result = term_db_read_by_id(1)
        assert result == {"id": 1, "name": "term_1"}
        mock_execute.assert_called_once_with("SELECT * FROM terms WHERE id = %s;", (1,))

    @patch("app.models.term.db.execute_query")
    def test_term_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = term_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.term.db.execute_query")
    def test_term_db_read_by_ids_empty_list(self, mock_execute):
        result = term_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.term.db.execute_query")
    def test_term_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"id": "t1"}, {"id": "t2"}]
        result = term_db_read_by_ids([1, 2])

        assert result == [{"id": "t1"}, {"id": "t2"}]
        mock_execute.assert_called_once()
        assert "IN (%s,%s)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.term.db.execute_query")
    def test_term_db_insert_success(self, mock_execute, valid_term_row):
        # For PostgreSQL, we expect dict format
        mock_execute.return_value = [{"id": 10}]
        params = (
            valid_term_row["name"],
            valid_term_row["start_date"],
            valid_term_row["end_date"],
        )

        result = term_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO terms" in query
        assert called_params == params

    @patch("app.models.term.db.execute_query")
    def test_term_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = term_db_insert(("bad",))
        assert result is None

    @patch("app.models.term.db.execute_query")
    def test_term_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = term_db_update(1, ("x",) * 3)  # name, start_date, end_date
        assert result == 1

    @patch("app.models.term.db.execute_query")
    def test_term_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = term_db_update(1, ("x",) * 3)
        assert result == 0

    @patch("app.models.term.db.execute_query")
    def test_term_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = term_db_archive(1)
        assert result == 1

    @patch("app.models.term.db.execute_query")
    def test_term_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = term_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestTermReadRoute:
    @patch("app.routes.term.get_all_terms")
    def test_handle_term_db_read_all_success(
        self, mock_get, client, valid_term_create_data
    ):
        mock_get.return_value = valid_term_create_data

        resp = client.get("/terms")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Terms fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_term_create_data
        mock_get.assert_called_once()

    @patch("app.routes.term.get_all_terms")
    def test_handle_term_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/terms")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.term.get_term_by_id")
    def test_handle_get_term_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "name": "Fall 2025"}

        response = client.get("/terms/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Term fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.term.get_term_by_id")
    def test_handle_get_term_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/terms/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Term not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.term.get_term_by_id")
    def test_handle_get_term_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/terms/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestTermCreateRoute:
    @patch("app.routes.term.create_new_terms")
    def test_handle_term_db_insert_success(
        self, mock_create_new_terms, client, valid_term_create_data
    ):
        mock_create_new_terms.return_value = (valid_term_create_data, None, None)

        response = client.post("/terms", json=valid_term_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 terms created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.term.create_new_terms")
    def test_handle_term_db_insert_service_error(
        self, mock_create_new_terms, client, valid_term_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_terms.return_value = ([], error_data, error_code)

        response = client.post("/terms", json=valid_term_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.term.create_new_terms")
    def test_handle_term_db_insert_key_error(
        self, mock_create_new_terms, client, valid_term_create_data
    ):
        mock_create_new_terms.side_effect = KeyError("name")

        response = client.post("/terms", json=valid_term_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.term.create_new_terms")
    def test_handle_term_db_insert_exception(
        self, mock_create_new_terms, client, valid_term_create_data
    ):
        mock_create_new_terms.side_effect = Exception("DB failure")

        response = client.post("/terms", json=valid_term_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestTermUpdateRoute:
    @patch("app.routes.term.update_terms")
    def test_handle_update_terms_success(
        self, mock_update_terms, client, valid_term_update_data
    ):
        mock_update_terms.return_value = (valid_term_update_data, None, None)

        response = client.put("/terms", json=valid_term_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Term updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.term.update_terms")
    def test_handle_update_terms_service_error(
        self, mock_update_terms, client, valid_term_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_terms.return_value = ([], error_data, error_code)

        response = client.put("/terms", json=valid_term_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.term.update_terms")
    def test_handle_update_terms_key_error(
        self, mock_update_terms, client, valid_term_update_data
    ):
        mock_update_terms.side_effect = KeyError("name")

        response = client.put("/terms", json=valid_term_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.term.update_terms")
    def test_handle_update_terms_exception(
        self, mock_update_terms, client, valid_term_update_data
    ):
        mock_update_terms.side_effect = Exception("DB failure")

        response = client.put("/terms", json=valid_term_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestTermArchiveRoute:
    @patch("app.routes.term.archive_terms")
    def test_handle_archive_terms_success(
        self, mock_archive_terms, client, valid_term_ids
    ):
        mock_archive_terms.return_value = (valid_term_ids, None, 200)

        response = client.patch("/terms", json={"ids": valid_term_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 terms archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.term.archive_terms")
    def test_handle_archive_terms_service_error(
        self, mock_archive_terms, client, valid_term_ids
    ):
        error_data = {"message": "No terms were archived."}
        error_code = 400
        mock_archive_terms.return_value = ([], error_data, error_code)

        response = client.patch("/terms", json={"ids": valid_term_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No terms were archived." in data["message"]

    @patch("app.routes.term.archive_terms")
    def test_handle_archive_terms_key_error(
        self, mock_archive_terms, client, valid_term_ids
    ):
        mock_archive_terms.side_effect = KeyError("ids")

        response = client.patch("/terms", json={"ids": valid_term_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.term.archive_terms")
    def test_handle_archive_terms_exception(
        self, mock_archive_terms, client, valid_term_ids
    ):
        mock_archive_terms.side_effect = Exception("DB failure")

        response = client.patch("/terms", json={"ids": valid_term_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
