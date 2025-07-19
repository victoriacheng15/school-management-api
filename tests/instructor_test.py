import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    read_all_active_instructors,
    read_instructor_by_id,
    create_instructor,
    update_instructor,
    archive_instructor,
    read_instructors_by_ids,
)
from app.services import (
    get_all_active_instructors,
    get_instructor_by_id,
    create_instructors,
    update_instructors,
    archive_instructors,
)

# =======================
# Fixtures
# =======================

def make_instructor_row():
    today = date.today().isoformat()
    return (
        1,
        "Alice",
        "Smith",
        "alice.smith@example.com",
        "456 College Ave",
        "ON",
        "full-time",
        "active",
        3,  # department_id
        today,
        today,
        0,  # is_archived
    )

def make_instructor_dict():
    return {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "address": "456 College Ave",
        "province": "ON",
        "employment": "full-time",
        "status": "active",
        "department_id": 3,
    }

@pytest.fixture
def valid_instructor_row():
    return make_instructor_row()

@pytest.fixture
def valid_instructor_rows():
    return [make_instructor_row() for _ in range(2)]

@pytest.fixture
def valid_instructor_create_data():
    return [
        make_instructor_dict(),
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "address": "789 University Rd",
            "province": "BC",
            "employment": "part-time",
            "status": "active",
            "department_id": 4,
        },
    ]

@pytest.fixture
def valid_instructor_update_data():
    data = make_instructor_dict()
    data["id"] = 1
    return [data]

@pytest.fixture
def instructor_missing_id(valid_instructor_update_data):
    data = [item.copy() for item in valid_instructor_update_data]
    for d in data:
        d.pop("id", None)
    return data

@pytest.fixture
def valid_instructor_ids():
    return [1, 2]

# =======================
# DB Mocks
# =======================

@pytest.fixture
def mock_db_read_all():
    with patch("app.services.instructor.read_all_active_instructors") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.instructor.read_instructor_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.instructor.read_instructors_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.instructor.create_instructor") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.instructor.update_instructor") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.instructor.archive_instructor") as mock:
        yield mock

# =======================
# Service Tests
# =======================
@pytest.skip 
class TestInstructorReadService:
    def test_get_all_active_instructors(mock_db_read_all, valid_instructor_row):
        mock_db_read_all.return_value = [valid_instructor_row]
        instructors = get_all_active_instructors()
        assert len(instructors) == 1
        assert instructors[0]["first_name"] == "Alice"
        mock_db_read_all.assert_called_once()

    def test_get_all_active_instructors_none(mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_active_instructors()

    def test_get_instructor_by_id(mock_db_read_one, valid_instructor_row):
        mock_db_read_one.return_value = valid_instructor_row
        instructor = get_instructor_by_id(1)
        assert instructor["first_name"] == "Alice"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_instructor_by_id_not_found(mock_db_read_one):
        mock_db_read_one.return_value = None
        instructor = get_instructor_by_id(999)
        assert instructor is None

@pytest.skip 
class TestInstructorCreateService:
    def test_create_instructors(
        mock_db_create, mock_db_read_many, valid_instructor_create_data, valid_instructor_rows
    ):
        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_instructor_rows

        created, error = create_instructors(valid_instructor_create_data)

        assert error is None
        assert len(created) == 2
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_instructors_failure(
        mock_db_create, mock_db_read_many, valid_instructor_create_data
    ):
        mock_db_create.side_effect = [None, None]
        created, error = create_instructors(valid_instructor_create_data)

        assert created == []
        assert error is None
        mock_db_read_many.assert_not_called()

@pytest.skip 
class TestInstructorUpdateService:
    def test_update_instructors(
        mock_db_update, mock_db_read_many, valid_instructor_update_data, valid_instructor_row
    ):
        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_instructor_row]

        updated, error = update_instructors(valid_instructor_update_data)

        assert error is None
        assert len(updated) == 1
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_instructors_no_success(
        mock_db_update, mock_db_read_many, valid_instructor_update_data
    ):
        mock_db_update.return_value = 0
        updated, error = update_instructors(valid_instructor_update_data)

        assert updated == []
        assert error is None
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_instructors_missing_id(
        mock_db_update, mock_db_read_many, instructor_missing_id
    ):
        updated, error = update_instructors(instructor_missing_id)

        assert updated == []
        assert error is None
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()

@pytest.skip 
class TestInstructorArchiveService:
    def test_archive_instructors(mock_db_archive, valid_instructor_ids):
        mock_db_archive.side_effect = [1, 1]
        archived = archive_instructors(valid_instructor_ids)

        assert len(archived) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_instructors_none_archived(mock_db_archive, valid_instructor_ids):
        mock_db_archive.return_value = 0
        archived = archive_instructors(valid_instructor_ids)

        assert archived == []

    def test_archive_instructors_invalid_ids():
        with pytest.raises(ValueError):
            archive_instructors(["one", 2])

# =======================
# Model Tests
# =======================
@pytest.skip 
class TestInstructorModel:
    @patch("app.models.instructor.db.execute_query")
    def test_read_all_active_instructors(mock_execute):
        mock_execute.return_value = [("mocked",)]
        result = read_all_active_instructors()
        assert result == [("mocked",)]
        mock_execute.assert_called_once_with(
            "SELECT * FROM instructors WHERE status = 'active';"
        )

    @patch("app.models.instructor.db.execute_query")
    def test_read_instructor_by_id_found(mock_execute):
        mock_execute.return_value = [("instructor_1",)]
        result = read_instructor_by_id(1)
        assert result == ("instructor_1",)
        mock_execute.assert_called_once_with("SELECT * FROM instructors WHERE id = ?;", (1,))

    @patch("app.models.instructor.db.execute_query")
    def test_read_instructor_by_id_not_found(mock_execute):
        mock_execute.return_value = []
        result = read_instructor_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.instructor.db.execute_query")
    def test_read_instructors_by_ids_empty_list(mock_execute):
        result = read_instructors_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.instructor.db.execute_query")
    def test_read_instructors_by_ids_success(mock_execute):
        mock_execute.return_value = [("i1",), ("i2",)]
        result = read_instructors_by_ids([1, 2])

        assert result == [("i1",), ("i2",)]
        mock_execute.assert_called_once()
        assert "IN (?,?)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.instructor.db.execute_query")
    def test_create_instructor_success(mock_execute, valid_instructor_row):
        mock_cursor = type("MockCursor", (), {"lastrowid": 10})()
        mock_execute.return_value = mock_cursor

        params = valid_instructor_row
        result = create_instructor(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO instructors" in query
        assert called_params == params

    @patch("app.models.instructor.db.execute_query")
    def test_create_instructor_failure(mock_execute):
        mock_execute.return_value = None
        result = create_instructor(("bad",))
        assert result is None

    @patch("app.models.instructor.db.execute_query")
    def test_update_instructor_success(mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = update_instructor(1, ("x",) * 10)
        assert result == 1

    @patch("app.models.instructor.db.execute_query")
    def test_update_instructor_failure(mock_execute):
        mock_execute.return_value = None
        result = update_instructor(1, ("x",) * 10)
        assert result == 0

    @patch("app.models.instructor.db.execute_query")
    def test_archive_instructor_success(mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = archive_instructor(1)
        assert result == 1

    @patch("app.models.instructor.db.execute_query")
    def test_archive_instructor_failure(mock_execute):
        mock_execute.return_value = None
        result = archive_instructor(999)
        assert result == 0

# =======================
# Route Tests
# =======================
@pytest.skip 
class TestInstructorReadRoute:
    @patch("app.routes.instructor.get_all_active_instructors")
    def test_handle_read_all_active_instructors_success(
        mock_get, client, valid_instructor_create_data
    ):
        mock_get.return_value = valid_instructor_create_data

        resp = client.get("/instructors")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Instructors fetched successfully" in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_instructor_create_data
        mock_get.assert_called_once()

    @patch("app.routes.instructor.get_all_active_instructors")
    def test_handle_read_all_active_instructors_exception(mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/instructors")
        data = response.get_json()

        assert response.status_code == 500
        assert "Unexpected error: DB failure" in data["error"]
        mock_get_all.assert_called_once()

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_success(mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "first_name": "Alice"}

        response = client.get("/instructors/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Instructor fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_not_found(mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/instructors/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Instructor not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_exception(mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/instructors/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "Unexpected error: DB error" in data["error"]
        mock_get_by_id.assert_called_once_with(1)

@pytest.skip 
class TestInstructorCreateRoute:
    @patch("app.routes.instructor.create_instructors")
    def test_handle_create_instructor_success(
        mock_create_instructors, client, valid_instructor_create_data
    ):
        mock_create_instructors.return_value = (valid_instructor_create_data, None, None)

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 instructors created successfully" in data["message"]
        assert isinstance(data["data"], dict) or isinstance(data["data"], list)

    @patch("app.routes.instructor.create_instructors")
    def test_handle_create_instructor_service_error(
        mock_create_instructors, client, valid_instructor_create_data
    ):
        error_data = {"error": "Invalid data"}
        error_code = 422
        mock_create_instructors.return_value = ([], error_data, error_code)

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["error"]

    @patch("app.routes.instructor.create_instructors")
    def test_handle_create_instructor_key_error(
        mock_create_instructors, client, valid_instructor_create_data
    ):
        mock_create_instructors.side_effect = KeyError("first_name")

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.instructor.create_instructors")
    def test_handle_create_instructor_exception(
        mock_create_instructors, client, valid_instructor_create_data
    ):
        mock_create_instructors.side_effect = Exception("DB failure")

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()

@pytest.skip 
class TestInstructorUpdateRoute:
    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_success(
        mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.return_value = (valid_instructor_update_data, None, None)

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Instructor updated successfully" in data["message"]
        assert isinstance(data["data"], dict) or isinstance(data["data"], list)

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_service_error(
        mock_update_instructors, client, valid_instructor_update_data
    ):
        error_data = {"error": "Invalid data"}
        error_code = 422
        mock_update_instructors.return_value = ([], error_data, error_code)

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["error"]

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_key_error(
        mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.side_effect = KeyError("first_name")

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_exception(
        mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.side_effect = Exception("DB failure")

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()


@pytest.skip 
class TestInstructorArchiveRoute:
    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_success(
        mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.return_value = valid_instructor_ids

        response = client.patch("/instructors", json=valid_instructor_ids)
        data = response.get_json()

        assert response.status_code == 200
        assert (
            f"{len(valid_instructor_ids)} instructor(s) archived successfully" in data["message"]
        )
        assert isinstance(data["data"], list)

    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_no_instructors_archived(
        mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.return_value = []

        response = client.patch("/instructors", json=valid_instructor_ids)
        data = response.get_json()

        assert response.status_code == 404
        assert "No instructors were archived" in data["error"]

    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_exception(
        mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.side_effect = Exception("DB failure")

        response = client.patch("/instructors", json=valid_instructor_ids)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()
