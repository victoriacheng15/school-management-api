import pytest
import os
from datetime import date
from unittest.mock import patch
from app.models import (
    assignment_db_read_all,
    assignment_db_read_by_id,
    assignment_db_read_by_ids,
    assignment_db_insert,
    assignment_db_update,
    assignment_db_archive,
)
from app.services import (
    get_all_assignments,
    get_assignment_by_id,
    create_new_assignments,
    update_assignments,
    archive_assignments,
)

# =======================
# Fixtures
# =======================


# Detect database type for tests
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite").lower()


def make_assignment_row():
    today = date.today().isoformat()
    if DATABASE_TYPE == "postgresql":
        return {
            "id": 1,
            "instructor_id": 1,
            "course_id": 1,
            "created_at": today,
            "updated_at": today,
            "is_archived": False,
        }
    else:
        return (
            1,
            1,
            1,
            today,
            today,
            0,
        )


def make_assignment_dict():
    return {
        "instructor_id": 1,
        "course_id": 1,
    }


@pytest.fixture
def valid_assignment_row():
    return make_assignment_row()


@pytest.fixture
def valid_assignment_rows():
    return [make_assignment_row() for _ in range(2)]


@pytest.fixture
def valid_assignment_create_data():
    return [
        make_assignment_dict(),
        {
            "instructor_id": 2,
            "course_id": 2,
        },
    ]


@pytest.fixture
def valid_assignment_update_data():
    data = make_assignment_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def assignment_missing_id(valid_assignment_update_data):
    data = [item.copy() for item in valid_assignment_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_assignment_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.assignment.assignment_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.assignment.assignment_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.assignment.assignment_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.assignment.assignment_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.assignment.assignment_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.assignment.assignment_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestAssignmentReadService:
    def test_get_all_assignments(self, mock_db_read_all, valid_assignment_row):
        # For SQLite, convert tuple fixture to dict to match model behavior
        if DATABASE_TYPE == "postgresql":
            mock_db_read_all.return_value = [valid_assignment_row]
        else:
            # For SQLite, convert tuple fixture to dict to match model behavior
            tuple_row = valid_assignment_row
            dict_row = {
                "id": tuple_row[0],
                "instructor_id": tuple_row[1],
                "course_id": tuple_row[2],
                "created_at": tuple_row[3],
                "updated_at": tuple_row[4],
                "is_archived": bool(tuple_row[5]),
            }
            mock_db_read_all.return_value = [dict_row]

        assignments = get_all_assignments(active_only=True)
        assert len(assignments) == 1
        assert assignments[0]["instructor_id"] == 1
        mock_db_read_all.assert_called_once()

    def test_get_all_assignments_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_assignments(active_only=True)

    def test_get_assignment_by_id(self, mock_db_read_one, valid_assignment_row):
        # Service layer expects dicts since model layer converts tuples to dicts
        if DATABASE_TYPE == "postgresql":
            mock_db_read_one.return_value = valid_assignment_row
        else:
            # For SQLite, convert tuple fixture to dict to match model behavior
            tuple_row = valid_assignment_row
            dict_row = {
                "id": tuple_row[0],
                "instructor_id": tuple_row[1],
                "course_id": tuple_row[2],
                "created_at": tuple_row[3],
                "updated_at": tuple_row[4],
                "is_archived": bool(tuple_row[5]),
            }
            mock_db_read_one.return_value = dict_row

        assignment = get_assignment_by_id(1)
        assert assignment["instructor_id"] == 1
        mock_db_read_one.assert_called_once_with(1)

    def test_get_assignment_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        assignment = get_assignment_by_id(123)
        assert assignment is None


class TestAssignmentCreateService:
    def test_create_new_assignments(
        self,
        mock_db_create,
        mock_db_read_many,
        valid_assignment_create_data,
        valid_assignment_rows,
    ):
        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_assignment_rows

        results, error, status_code = create_new_assignments(
            valid_assignment_create_data
        )

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_assignments_failure(
        self, mock_db_create, mock_db_read_many, valid_assignment_create_data
    ):
        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_assignments(
            valid_assignment_create_data
        )

        assert results == []
        assert error["message"] == "No assignments were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


class TestAssignmentUpdateService:
    @patch("app.models.assignment.db")  # Mock the db instance  
    @patch("app.services.assignment.assignment_dict_to_row")
    def test_update_assignments(
        self,
        mock_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_assignment_update_data,
        valid_assignment_row,
    ):
        # This test is fully mocked and does not require a real DB connection
        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_assignment_row]
        
        # For SQLite, we need to ensure row is converted to dict properly
        if isinstance(valid_assignment_row, tuple):
            mock_existing_dict = {
                "id": valid_assignment_row[0],
                "instructor_id": valid_assignment_row[1],
                "course_id": valid_assignment_row[2],
                "created_at": valid_assignment_row[3],
                "updated_at": valid_assignment_row[4],
                "is_archived": bool(valid_assignment_row[5]),
            }
            mock_db_read_one.return_value = mock_existing_dict
        else:
            mock_db_read_one.return_value = valid_assignment_row
            
        mock_dict_to_row.return_value = (1, 1)  # Mock conversion

        results, error, status_code = update_assignments(valid_assignment_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    @patch("app.models.assignment.db")  # Mock the db instance  
    @patch("app.services.assignment.assignment_dict_to_row")
    def test_update_assignments_no_success(
        self,
        mock_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_assignment_update_data,
        valid_assignment_row,
    ):
        mock_db_update.return_value = 0  # Simulate no update
        
        # For SQLite, we need to ensure row is converted to dict properly
        if isinstance(valid_assignment_row, tuple):
            mock_existing_dict = {
                "id": valid_assignment_row[0],
                "instructor_id": valid_assignment_row[1],
                "course_id": valid_assignment_row[2],
                "created_at": valid_assignment_row[3],
                "updated_at": valid_assignment_row[4],
                "is_archived": bool(valid_assignment_row[5]),
            }
            mock_db_read_one.return_value = mock_existing_dict
        else:
            mock_db_read_one.return_value = valid_assignment_row
            
        mock_dict_to_row.return_value = (1, 1)  # Mock conversion
        
        results, error, status_code = update_assignments(valid_assignment_update_data)

        assert results == []
        assert error == [{"message": "Assignment ID 1 not updated."}]
        assert status_code == 400
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_not_called()

    @patch("app.models.assignment.db")  # Mock the db instance  
    @patch("app.services.assignment.assignment_dict_to_row")
    def test_update_assignments_missing_id(
        self,
        mock_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        assignment_missing_id,
    ):
        results, error, status_code = update_assignments(assignment_missing_id)

        assert results == []
        assert error == [{"message": "Missing assignment ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


class TestAssignmentArchiveService:
    @patch("app.models.assignment.db")  # Mock the db instance
    def test_archive_assignments(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_assignment_ids,
        valid_assignment_row,
    ):
        mock_db_archive.side_effect = [1, 1]
        mock_db_read_one.return_value = valid_assignment_row  # Mock get_existing_func
        mock_db_read_many.return_value = [valid_assignment_row, valid_assignment_row]  # Mock read_by_ids_func
        archived = archive_assignments(valid_assignment_ids)

        assert len(archived[0]) == 2
        assert mock_db_archive.call_count == 2

    @patch("app.models.assignment.db")  # Mock the db instance
    def test_archive_assignments_none_archived(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_assignment_ids,
        valid_assignment_row,
    ):
        mock_db_archive.return_value = 0
        mock_db_read_one.return_value = valid_assignment_row  # Mock get_existing_func
        archived = archive_assignments(valid_assignment_ids)

        assert archived[0] == []

    def test_archive_assignments_invalid_ids(self):
        results, errors, status = archive_assignments(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestAssignmentModel:
    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": "data"}]
        result = assignment_db_read_all()
        assert result == [{"mocked": "data"}]
        mock_execute.assert_called_once_with("SELECT * FROM assignments;")

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [{"active": "assignment"}]
        result = assignment_db_read_all(active_only=True)
        assert result == [{"active": "assignment"}]
        if DATABASE_TYPE == "postgresql":
            mock_execute.assert_called_once_with(
                "SELECT * FROM assignments WHERE is_archived = FALSE;"
            )
        else:
            mock_execute.assert_called_once_with(
                "SELECT * FROM assignments WHERE is_archived = 0;"
            )

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"id": 1, "instructor_id": 1}]
        result = assignment_db_read_by_id(1)
        assert result == {"id": 1, "instructor_id": 1}
        mock_execute.assert_called_once_with(
            "SELECT * FROM assignments WHERE id = ?;", (1,)
        )

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = assignment_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_by_ids_empty_list(self, mock_execute):
        result = assignment_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"id": 1}, {"id": 2}]
        result = assignment_db_read_by_ids([1, 2])

        assert result == [{"id": 1}, {"id": 2}]
        mock_execute.assert_called_once()

        query_call = mock_execute.call_args.args[0]
        assert "IN (?,?)" in query_call
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_insert_success(self, mock_execute, valid_assignment_row):
        # For PostgreSQL, we expect dict format, for SQLite tuple format
        if DATABASE_TYPE == "postgresql":
            mock_execute.return_value = [{"id": 10}]
            params = (
                valid_assignment_row["instructor_id"],
                valid_assignment_row["course_id"],
            )
        else:
            mock_cursor = type("MockCursor", (), {"lastrowid": 10})()
            mock_execute.return_value = mock_cursor
            params = valid_assignment_row

        result = assignment_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO assignments" in query
        assert called_params == params

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = assignment_db_insert(("bad",))
        assert result is None

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = assignment_db_update(1, ("x",) * 2)
        assert result == 1

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = assignment_db_update(1, ("x",) * 2)
        assert result == 0

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = assignment_db_archive(1)
        assert result == 1

    @patch("app.models.assignment.db.execute_query")
    def test_assignment_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = assignment_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestAssignmentReadRoute:
    @patch("app.routes.assignment.get_all_assignments")
    def test_handle_assignment_db_read_all_success(
        self, mock_get, client, valid_assignment_create_data
    ):
        mock_get.return_value = valid_assignment_create_data

        resp = client.get("/assignments")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Assignments fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_assignment_create_data
        mock_get.assert_called_once()

    @patch("app.routes.assignment.get_all_assignments")
    def test_handle_assignment_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/assignments")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.assignment.get_assignment_by_id")
    def test_handle_get_assignment_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "instructor_id": 1}

        response = client.get("/assignments/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Assignment fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.assignment.get_assignment_by_id")
    def test_handle_get_assignment_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/assignments/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Assignment not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.assignment.get_assignment_by_id")
    def test_handle_get_assignment_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/assignments/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestAssignmentCreateRoute:
    @patch("app.routes.assignment.create_new_assignments")
    def test_handle_assignment_db_insert_success(
        self, mock_create_new_assignments, client, valid_assignment_create_data
    ):
        mock_create_new_assignments.return_value = (
            valid_assignment_create_data,
            None,
            None,
        )

        response = client.post("/assignments", json=valid_assignment_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 assignments created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.assignment.create_new_assignments")
    def test_handle_assignment_db_insert_service_error(
        self, mock_create_new_assignments, client, valid_assignment_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_assignments.return_value = ([], error_data, error_code)

        response = client.post("/assignments", json=valid_assignment_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.assignment.create_new_assignments")
    def test_handle_assignment_db_insert_key_error(
        self, mock_create_new_assignments, client, valid_assignment_create_data
    ):
        mock_create_new_assignments.side_effect = KeyError("instructor_id")

        response = client.post("/assignments", json=valid_assignment_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.assignment.create_new_assignments")
    def test_handle_assignment_db_insert_exception(
        self, mock_create_new_assignments, client, valid_assignment_create_data
    ):
        mock_create_new_assignments.side_effect = Exception("DB failure")

        response = client.post("/assignments", json=valid_assignment_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestAssignmentUpdateRoute:
    @patch("app.routes.assignment.update_assignments")
    def test_handle_update_assignments_success(
        self, mock_update_assignments, client, valid_assignment_update_data
    ):
        mock_update_assignments.return_value = (
            valid_assignment_update_data,
            None,
            None,
        )

        response = client.put("/assignments", json=valid_assignment_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Assignment updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.assignment.update_assignments")
    def test_handle_update_assignments_service_error(
        self, mock_update_assignments, client, valid_assignment_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_assignments.return_value = ([], error_data, error_code)

        response = client.put("/assignments", json=valid_assignment_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.assignment.update_assignments")
    def test_handle_update_assignments_key_error(
        self, mock_update_assignments, client, valid_assignment_update_data
    ):
        mock_update_assignments.side_effect = KeyError("instructor_id")

        response = client.put("/assignments", json=valid_assignment_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.assignment.update_assignments")
    def test_handle_update_assignments_exception(
        self, mock_update_assignments, client, valid_assignment_update_data
    ):
        mock_update_assignments.side_effect = Exception("DB failure")

        response = client.put("/assignments", json=valid_assignment_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestAssignmentArchiveRoute:
    @patch("app.routes.assignment.archive_assignments")
    def test_handle_archive_assignments_success(
        self, mock_archive_assignments, client, valid_assignment_ids
    ):
        mock_archive_assignments.return_value = (valid_assignment_ids, None, 200)

        response = client.patch("/assignments", json={"ids": valid_assignment_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 assignments archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.assignment.archive_assignments")
    def test_handle_archive_assignments_service_error(
        self, mock_archive_assignments, client, valid_assignment_ids
    ):
        error_data = {"message": "No assignments were archived."}
        error_code = 400
        mock_archive_assignments.return_value = ([], error_data, error_code)

        response = client.patch("/assignments", json={"ids": valid_assignment_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No assignments were archived." in data["message"]

    @patch("app.routes.assignment.archive_assignments")
    def test_handle_archive_assignments_key_error(
        self, mock_archive_assignments, client, valid_assignment_ids
    ):
        mock_archive_assignments.side_effect = KeyError("ids")

        response = client.patch("/assignments", json={"ids": valid_assignment_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.assignment.archive_assignments")
    def test_handle_archive_assignments_exception(
        self, mock_archive_assignments, client, valid_assignment_ids
    ):
        mock_archive_assignments.side_effect = Exception("DB failure")

        response = client.patch("/assignments", json={"ids": valid_assignment_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
