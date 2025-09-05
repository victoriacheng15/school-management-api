import pytest
import os
from datetime import date
from unittest.mock import patch
from app.models import (
    enrollment_db_read_all,
    enrollment_db_read_by_id,
    enrollment_db_read_by_ids,
    enrollment_db_insert,
    enrollment_db_update,
    enrollment_db_archive,
)
from app.services import (
    get_all_enrollments,
    get_enrollment_by_id,
    create_new_enrollments,
    update_enrollments,
    archive_enrollments,
)

# Detect database type for tests
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite").lower()

# =======================
# Fixtures
# =======================


def make_enrollment_row():
    today = date.today().isoformat()

    if DATABASE_TYPE == "postgresql":
        # PostgreSQL returns dict-like objects
        return {
            "id": 1,
            "student_id": 1,
            "course_id": 1,
            "grade": "A",
            "created_at": today,
            "updated_at": today,
            "is_archived": False,
        }
    else:
        # SQLite returns tuple objects
        return (
            1,
            1,
            1,
            "A",
            today,
            today,
            0,
        )


def make_enrollment_dict():
    return {
        "student_id": 1,
        "course_id": 1,
        "grade": "A",
    }


@pytest.fixture
def valid_enrollment_row():
    return make_enrollment_row()


@pytest.fixture
def valid_enrollment_rows():
    return [make_enrollment_row() for _ in range(2)]


@pytest.fixture
def valid_enrollment_create_data():
    return [
        make_enrollment_dict(),
        {
            "student_id": 2,
            "course_id": 2,
            "grade": "B",
        },
    ]


@pytest.fixture
def valid_enrollment_update_data():
    data = make_enrollment_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def enrollment_missing_id(valid_enrollment_update_data):
    data = [item.copy() for item in valid_enrollment_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_enrollment_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.enrollment.enrollment_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.enrollment.enrollment_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.enrollment.enrollment_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.enrollment.enrollment_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.enrollment.enrollment_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.enrollment.enrollment_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestEnrollmentReadService:
    def test_get_all_enrollments(self, mock_db_read_all, valid_enrollment_row):
        # For SQLite, convert tuple fixture to dict to match model behavior
        if DATABASE_TYPE == "postgresql":
            mock_db_read_all.return_value = [valid_enrollment_row]
        else:
            # For SQLite, convert tuple fixture to dict to match model behavior
            tuple_row = valid_enrollment_row
            dict_row = {
                "id": tuple_row[0],
                "student_id": tuple_row[1],
                "course_id": tuple_row[2],
                "grade": tuple_row[3],
                "created_at": tuple_row[4],
                "updated_at": tuple_row[5],
                "is_archived": bool(tuple_row[6]),
            }
            mock_db_read_all.return_value = [dict_row]

        enrollments = get_all_enrollments(active_only=True)
        assert len(enrollments) == 1
        assert enrollments[0]["grade"] == "A"
        mock_db_read_all.assert_called_once()

    def test_get_all_enrollments_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_enrollments(active_only=True)

    def test_get_enrollment_by_id(self, mock_db_read_one, valid_enrollment_row):
        # Service layer expects dicts since model layer converts tuples to dicts
        if DATABASE_TYPE == "postgresql":
            mock_db_read_one.return_value = valid_enrollment_row
        else:
            # For SQLite, convert tuple fixture to dict to match model behavior
            tuple_row = valid_enrollment_row
            dict_row = {
                "id": tuple_row[0],
                "student_id": tuple_row[1],
                "course_id": tuple_row[2],
                "grade": tuple_row[3],
                "created_at": tuple_row[4],
                "updated_at": tuple_row[5],
                "is_archived": bool(tuple_row[6]),
            }
            mock_db_read_one.return_value = dict_row

        enrollment = get_enrollment_by_id(1)
        assert enrollment["grade"] == "A"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_enrollment_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        enrollment = get_enrollment_by_id(123)
        assert enrollment is None


class TestEnrollmentCreateService:
    def test_create_new_enrollments(
        self,
        mock_db_create,
        mock_db_read_many,
        valid_enrollment_create_data,
        valid_enrollment_rows,
    ):
        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_enrollment_rows

        results, error, status_code = create_new_enrollments(
            valid_enrollment_create_data
        )

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_enrollments_failure(
        self, mock_db_create, mock_db_read_many, valid_enrollment_create_data
    ):
        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_enrollments(
            valid_enrollment_create_data
        )

        assert results == []
        assert error["message"] == "No enrollments were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


class TestEnrollmentUpdateService:
    def test_update_enrollments(
        self,
        mock_db_update,
        mock_db_read_many,
        valid_enrollment_update_data,
        valid_enrollment_row,
    ):
        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_enrollment_row]

        results, error, status_code = update_enrollments(valid_enrollment_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_enrollments_no_success(
        self, mock_db_update, mock_db_read_many, valid_enrollment_update_data
    ):
        mock_db_update.return_value = 0
        results, error, status_code = update_enrollments(valid_enrollment_update_data)

        assert results == []
        assert error == [{"message": "Enrollment ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_enrollments_missing_id(
        self, mock_db_update, mock_db_read_many, enrollment_missing_id
    ):
        results, error, status_code = update_enrollments(enrollment_missing_id)

        assert results == []
        assert error == [{"message": "Missing enrollment ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


class TestEnrollmentArchiveService:
    def test_archive_enrollments(self, mock_db_archive, valid_enrollment_ids):
        mock_db_archive.side_effect = [1, 1]
        archived, errors, status_code = archive_enrollments(valid_enrollment_ids)

        assert len(archived) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_enrollments_none_archived(
        self, mock_db_archive, valid_enrollment_ids
    ):
        mock_db_archive.return_value = 0
        archived, errors, status_code = archive_enrollments(valid_enrollment_ids)

        assert archived == []

    def test_archive_enrollments_invalid_ids(self):
        results, errors, status = archive_enrollments(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestEnrollmentModel:
    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": "data"}]
        result = enrollment_db_read_all()
        assert result == [{"mocked": "data"}]
        mock_execute.assert_called_once_with("SELECT * FROM enrollments;")

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"enrollment_1": "data"}]
        result = enrollment_db_read_by_id(1)
        assert result == {"enrollment_1": "data"}
        # The model uses SQLite syntax (?), database layer converts internally
        mock_execute.assert_called_once_with(
            "SELECT * FROM enrollments WHERE id = ?;", (1,)
        )

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = enrollment_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_read_by_ids_empty_list(self, mock_execute):
        result = enrollment_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"e1": "data"}, {"e2": "data"}]
        result = enrollment_db_read_by_ids([1, 2])

        assert result == [{"e1": "data"}, {"e2": "data"}]
        mock_execute.assert_called_once()

        # The model uses SQLite syntax (?), database layer converts internally
        query_call = mock_execute.call_args.args[0]
        assert "IN (?,?)" in query_call
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_insert_success(self, mock_execute, valid_enrollment_row):
        # For PostgreSQL, we expect dict format, for SQLite tuple format
        if DATABASE_TYPE == "postgresql":
            # PostgreSQL returns the inserted row with RETURNING clause
            mock_execute.return_value = [{"id": 10}]
            params = (
                valid_enrollment_row["student_id"],
                valid_enrollment_row["course_id"],
                valid_enrollment_row["grade"],
            )
        else:
            # SQLite returns cursor with lastrowid
            mock_cursor = type("MockCursor", (), {"lastrowid": 10})()
            mock_execute.return_value = mock_cursor
            params = valid_enrollment_row[1:4]  # student_id, course_id, grade

        result = enrollment_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO enrollments" in query
        assert called_params == params

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = enrollment_db_insert(("bad",))
        assert result is None

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = enrollment_db_update(1, ("x",) * 3)  # student_id, course_id, grade
        assert result == 1

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = enrollment_db_update(1, ("x",) * 3)
        assert result == 0

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = enrollment_db_archive(1)
        assert result == 1

    @patch("app.models.enrollment.db.execute_query")
    def test_enrollment_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = enrollment_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestEnrollmentReadRoute:
    @patch("app.routes.enrollment.get_all_enrollments")
    def test_handle_enrollment_db_read_all_success(
        self, mock_get, client, valid_enrollment_create_data
    ):
        mock_get.return_value = valid_enrollment_create_data

        resp = client.get("/enrollments")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Enrollments fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_enrollment_create_data
        mock_get.assert_called_once()

    @patch("app.routes.enrollment.get_all_enrollments")
    def test_handle_enrollment_db_read_all_with_active_only(
        self, mock_get, client, valid_enrollment_create_data
    ):
        mock_get.return_value = valid_enrollment_create_data

        resp = client.get("/enrollments?active_only=true")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Enrollments fetched successfully." in data["message"]
        mock_get.assert_called_once_with(active_only=True)

    @patch("app.routes.enrollment.get_all_enrollments")
    def test_handle_enrollment_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/enrollments")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.enrollment.get_enrollment_by_id")
    def test_handle_get_enrollment_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "grade": "A"}

        response = client.get("/enrollments/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Enrollment fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.enrollment.get_enrollment_by_id")
    def test_handle_get_enrollment_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/enrollments/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Enrollment not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.enrollment.get_enrollment_by_id")
    def test_handle_get_enrollment_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/enrollments/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()


class TestEnrollmentCreateRoute:
    @patch("app.routes.enrollment.create_new_enrollments")
    def test_handle_enrollment_db_insert_success(
        self, mock_create_new_enrollments, client, valid_enrollment_create_data
    ):
        mock_create_new_enrollments.return_value = (
            valid_enrollment_create_data,
            None,
            None,
        )

        response = client.post("/enrollments", json=valid_enrollment_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 enrollments created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.enrollment.create_new_enrollments")
    def test_handle_enrollment_db_insert_service_error(
        self, mock_create_new_enrollments, client, valid_enrollment_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_enrollments.return_value = ([], error_data, error_code)

        response = client.post("/enrollments", json=valid_enrollment_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.enrollment.create_new_enrollments")
    def test_handle_enrollment_db_insert_key_error(
        self, mock_create_new_enrollments, client, valid_enrollment_create_data
    ):
        mock_create_new_enrollments.side_effect = KeyError("student_id")

        response = client.post("/enrollments", json=valid_enrollment_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.enrollment.create_new_enrollments")
    def test_handle_enrollment_db_insert_exception(
        self, mock_create_new_enrollments, client, valid_enrollment_create_data
    ):
        mock_create_new_enrollments.side_effect = Exception("DB failure")

        response = client.post("/enrollments", json=valid_enrollment_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestEnrollmentUpdateRoute:
    @patch("app.routes.enrollment.update_enrollments")
    def test_handle_update_enrollments_success(
        self, mock_update_enrollments, client, valid_enrollment_update_data
    ):
        mock_update_enrollments.return_value = (
            valid_enrollment_update_data,
            None,
            None,
        )

        response = client.put("/enrollments", json=valid_enrollment_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Enrollment updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.enrollment.update_enrollments")
    def test_handle_update_enrollments_service_error(
        self, mock_update_enrollments, client, valid_enrollment_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_enrollments.return_value = ([], error_data, error_code)

        response = client.put("/enrollments", json=valid_enrollment_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.enrollment.update_enrollments")
    def test_handle_update_enrollments_key_error(
        self, mock_update_enrollments, client, valid_enrollment_update_data
    ):
        mock_update_enrollments.side_effect = KeyError("student_id")

        response = client.put("/enrollments", json=valid_enrollment_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.enrollment.update_enrollments")
    def test_handle_update_enrollments_exception(
        self, mock_update_enrollments, client, valid_enrollment_update_data
    ):
        mock_update_enrollments.side_effect = Exception("DB failure")

        response = client.put("/enrollments", json=valid_enrollment_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestEnrollmentArchiveRoute:
    @patch("app.routes.enrollment.archive_enrollments")
    def test_handle_archive_enrollments_success(
        self, mock_archive_enrollments, client, valid_enrollment_ids
    ):
        mock_archive_enrollments.return_value = (valid_enrollment_ids, None, 200)

        response = client.patch("/enrollments", json={"ids": valid_enrollment_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 enrollments archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.enrollment.archive_enrollments")
    def test_handle_archive_enrollments_service_error(
        self, mock_archive_enrollments, client, valid_enrollment_ids
    ):
        error_data = {"message": "No enrollments were archived."}
        error_code = 400
        mock_archive_enrollments.return_value = ([], error_data, error_code)

        response = client.patch("/enrollments", json={"ids": valid_enrollment_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No enrollments were archived." in data["message"]

    @patch("app.routes.enrollment.archive_enrollments")
    def test_handle_archive_enrollments_key_error(
        self, mock_archive_enrollments, client, valid_enrollment_ids
    ):
        mock_archive_enrollments.side_effect = KeyError("ids")

        response = client.patch("/enrollments", json={"ids": valid_enrollment_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.enrollment.archive_enrollments")
    def test_handle_archive_enrollments_exception(
        self, mock_archive_enrollments, client, valid_enrollment_ids
    ):
        mock_archive_enrollments.side_effect = Exception("DB failure")

        response = client.patch("/enrollments", json={"ids": valid_enrollment_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
