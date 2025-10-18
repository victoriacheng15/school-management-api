import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    instructor_db_read_all,
    instructor_db_read_by_id,
    instructor_db_read_by_ids,
    instructor_db_insert,
    instructor_db_update,
    instructor_db_archive,
)
from app.services import (
    get_all_instructors,
    get_instructor_by_id,
    create_new_instructors,
    update_instructors,
    archive_instructors,
)

# =======================
# Fixtures
# =======================


def make_instructor_row():
    today = date.today().isoformat()
    return {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "address": "123 Main St",
        "province": "ON",
        "employment": "full-time",
        "status": "active",
        "department_id": 1,
        "created_at": today,
        "updated_at": today,
        "is_archived": False,
    }


def make_instructor_dict():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "department_id": 1,
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
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "department_id": 2,
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
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.instructor.instructor_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.instructor.instructor_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.instructor.instructor_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.instructor.instructor_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.instructor.instructor_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.instructor.instructor_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestInstructorReadService:
    def test_get_all_instructors(self, mock_db_read_all, valid_instructor_row):
        mock_db_read_all.return_value = [valid_instructor_row]

        instructors = get_all_instructors(active_only=True)
        assert len(instructors) == 1
        assert instructors[0]["first_name"] == "John"
        mock_db_read_all.assert_called_once()

    def test_get_all_instructors_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_instructors(active_only=True)

    def test_get_instructor_by_id(self, mock_db_read_one, valid_instructor_row):
        mock_db_read_one.return_value = valid_instructor_row

        instructor = get_instructor_by_id(1)
        assert instructor["first_name"] == "John"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_instructor_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        instructor = get_instructor_by_id(123)
        assert instructor is None


@patch("app.models.instructor.db")
@patch("app.services.instructor.instructor_dict_to_row")
class TestInstructorCreateService:
    def test_create_new_instructors(
        self,
        mock_instructor_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_instructor_create_data,
        valid_instructor_rows,
    ):
        # Mock the instructor_dict_to_row function
        mock_instructor_dict_to_row.return_value = (
            "John",
            "Doe",
            "johndoe@example.com",
            "123 Main St",
            "Anytown",
            "Full-Time",
            "active",
            1,
        )

        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_instructor_rows

        results, error, status_code = create_new_instructors(
            valid_instructor_create_data
        )

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_instructors_failure(
        self,
        mock_instructor_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_instructor_create_data,
    ):
        # Mock the instructor_dict_to_row function
        mock_instructor_dict_to_row.return_value = (
            "John",
            "Doe",
            "johndoe@example.com",
            "123 Main St",
            "Anytown",
            "Full-Time",
            "active",
            1,
        )

        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_instructors(
            valid_instructor_create_data
        )

        assert results == []
        assert error["message"] == "No instructors were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


@patch("app.models.instructor.db")
@patch("app.services.instructor.instructor_dict_to_row")
class TestInstructorUpdateService:
    def test_update_instructors(
        self,
        mock_instructor_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_instructor_update_data,
        valid_instructor_row,
    ):
        # Mock the instructor_dict_to_row function
        mock_instructor_dict_to_row.return_value = (
            "John",
            "Doe",
            "johndoe@example.com",
            "123 Main St",
            "Anytown",
            "Full-Time",
            "active",
            1,
        )

        mock_db_read_one.return_value = valid_instructor_row

        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_instructor_row]

        results, error, status_code = update_instructors(valid_instructor_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_instructors_no_success(
        self,
        mock_instructor_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_instructor_update_data,
        valid_instructor_row,
    ):
        # Mock the instructor_dict_to_row function
        mock_instructor_dict_to_row.return_value = (
            "John",
            "Doe",
            "johndoe@example.com",
            "123 Main St",
            "Anytown",
            "Full-Time",
            "active",
            1,
        )

        mock_db_read_one.return_value = valid_instructor_row

        mock_db_update.return_value = 0
        results, error, status_code = update_instructors(valid_instructor_update_data)

        assert results == []
        assert error == [{"message": "Instructor ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_instructors_missing_id(
        self,
        mock_instructor_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        instructor_missing_id,
    ):
        results, error, status_code = update_instructors(instructor_missing_id)

        assert results == []
        assert error == [{"message": "Missing instructor ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


@patch("app.models.instructor.db")
class TestInstructorArchiveService:
    def test_archive_instructors(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_instructor_ids,
        valid_instructor_row,
    ):
        # Mock that instructors exist
        mock_db_read_one.return_value = valid_instructor_row
        mock_db_read_many.return_value = [
            valid_instructor_row,
            valid_instructor_row,
        ]

        mock_db_archive.side_effect = [1, 1]
        archived, errors, status_code = archive_instructors(valid_instructor_ids)

        assert len(archived) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_instructors_none_archived(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_instructor_ids,
        valid_instructor_row,
    ):
        # Mock that instructors exist
        mock_db_read_one.return_value = valid_instructor_row

        mock_db_archive.return_value = 0
        archived, errors, status_code = archive_instructors(valid_instructor_ids)

        assert archived == []

    def test_archive_instructors_invalid_ids(
        self, mock_db_instance, mock_db_archive, mock_db_read_one, mock_db_read_many
    ):
        results, errors, status = archive_instructors(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestInstructorModel:
    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": "data"}]
        result = instructor_db_read_all()
        assert result == [{"mocked": "data"}]
        mock_execute.assert_called_once_with("SELECT * FROM instructors;")

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [{"active": "instructor"}]
        result = instructor_db_read_all(active_only=True)
        assert result == [{"active": "instructor"}]
        mock_execute.assert_called_once_with(
            "SELECT * FROM instructors WHERE status = 'active';"
        )

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"id": 1, "first_name": "John"}]
        result = instructor_db_read_by_id(1)
        assert result == {"id": 1, "first_name": "John"}
        # The model uses PostgreSQL syntax (%s)
        mock_execute.assert_called_once_with(
            "SELECT * FROM instructors WHERE id = %s;", (1,)
        )

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = instructor_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_by_ids_empty_list(self, mock_execute):
        result = instructor_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"id": 1}, {"id": 2}]
        result = instructor_db_read_by_ids([1, 2])

        assert result == [{"id": 1}, {"id": 2}]
        mock_execute.assert_called_once()

        # The model uses PostgreSQL syntax (%s)
        query_call = mock_execute.call_args.args[0]
        assert "IN (%s,%s)" in query_call
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_insert_success(self, mock_execute, valid_instructor_row):
        # PostgreSQL returns the inserted row with RETURNING clause
        mock_execute.return_value = [{"id": 10}]
        params = (
            valid_instructor_row["first_name"],
            valid_instructor_row["last_name"],
            valid_instructor_row["email"],
            valid_instructor_row["address"],
            valid_instructor_row["province"],
            valid_instructor_row["employment"],
            valid_instructor_row["status"],
            valid_instructor_row["department_id"],
        )

        result = instructor_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO instructors" in query
        assert called_params == params

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = instructor_db_insert(("bad",))
        assert result is None

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = instructor_db_update(1, ("x",) * 8)
        assert result == 1

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = instructor_db_update(1, ("x",) * 8)
        assert result == 0

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = instructor_db_archive(1)
        assert result == 1

    @patch("app.models.instructor.db.execute_query")
    def test_instructor_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = instructor_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestInstructorReadRoute:
    @patch("app.routes.instructor.get_all_instructors")
    def test_handle_instructor_db_read_all_success(
        self, mock_get, client, valid_instructor_create_data
    ):
        mock_get.return_value = valid_instructor_create_data

        resp = client.get("/instructors")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Instructors fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_instructor_create_data
        mock_get.assert_called_once()

    @patch("app.routes.instructor.get_all_instructors")
    def test_handle_instructor_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/instructors")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "first_name": "John"}

        response = client.get("/instructors/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Instructor fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/instructors/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Instructor not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.instructor.get_instructor_by_id")
    def test_handle_get_instructor_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/instructors/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestInstructorCreateRoute:
    @patch("app.routes.instructor.create_new_instructors")
    def test_handle_instructor_db_insert_success(
        self, mock_create_new_instructors, client, valid_instructor_create_data
    ):
        mock_create_new_instructors.return_value = (
            valid_instructor_create_data,
            None,
            None,
        )

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 instructors created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.instructor.create_new_instructors")
    def test_handle_instructor_db_insert_service_error(
        self, mock_create_new_instructors, client, valid_instructor_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_instructors.return_value = ([], error_data, error_code)

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.instructor.create_new_instructors")
    def test_handle_instructor_db_insert_key_error(
        self, mock_create_new_instructors, client, valid_instructor_create_data
    ):
        mock_create_new_instructors.side_effect = KeyError("first_name")

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.instructor.create_new_instructors")
    def test_handle_instructor_db_insert_exception(
        self, mock_create_new_instructors, client, valid_instructor_create_data
    ):
        mock_create_new_instructors.side_effect = Exception("DB failure")

        response = client.post("/instructors", json=valid_instructor_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestInstructorUpdateRoute:
    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_success(
        self, mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.return_value = (
            valid_instructor_update_data,
            None,
            None,
        )

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Instructor updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_service_error(
        self, mock_update_instructors, client, valid_instructor_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_instructors.return_value = ([], error_data, error_code)

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_key_error(
        self, mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.side_effect = KeyError("first_name")

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.instructor.update_instructors")
    def test_handle_update_instructors_exception(
        self, mock_update_instructors, client, valid_instructor_update_data
    ):
        mock_update_instructors.side_effect = Exception("DB failure")

        response = client.put("/instructors", json=valid_instructor_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestInstructorArchiveRoute:
    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_success(
        self, mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.return_value = (valid_instructor_ids, None, 200)

        response = client.patch("/instructors", json={"ids": valid_instructor_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 instructors archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_service_error(
        self, mock_archive_instructors, client, valid_instructor_ids
    ):
        error_data = {"message": "No instructors were archived."}
        error_code = 400
        mock_archive_instructors.return_value = ([], error_data, error_code)

        response = client.patch("/instructors", json={"ids": valid_instructor_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No instructors were archived." in data["message"]

    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_key_error(
        self, mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.side_effect = KeyError("ids")

        response = client.patch("/instructors", json={"ids": valid_instructor_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.instructor.archive_instructors")
    def test_handle_archive_instructors_exception(
        self, mock_archive_instructors, client, valid_instructor_ids
    ):
        mock_archive_instructors.side_effect = Exception("DB failure")

        response = client.patch("/instructors", json={"ids": valid_instructor_ids})
        data = response.get_json()
        print(data)

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
