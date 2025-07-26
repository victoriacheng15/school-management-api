import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    department_db_read_all,
    department_db_read_by_id,
    department_db_read_by_ids,
    department_db_insert,
    department_db_update,
    department_db_archive,
)
from app.services import (
    get_all_departments,
    get_department_by_id,
    create_new_departments,
    update_departments,
    archive_departments,
)

# =======================
# Fixtures
# =======================


def make_department_row():
    today = date.today().isoformat()
    return (
        1,
        "Computer Science",
        today,
        today,
        0,
    )


def make_department_dict():
    return {
        "name": "Computer Science",
    }


@pytest.fixture
def valid_department_row():
    return make_department_row()


@pytest.fixture
def valid_department_rows():
    return [make_department_row() for _ in range(2)]


@pytest.fixture
def valid_department_create_data():
    return [
        make_department_dict(),
        {
            "name": "Business",
        },
    ]


@pytest.fixture
def valid_department_update_data():
    data = make_department_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def department_missing_id(valid_department_update_data):
    data = [item.copy() for item in valid_department_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_department_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.department.department_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.department.department_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.department.department_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.department.department_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.department.department_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.department.department_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestDepartmentReadService:
    def test_get_all_departments(self, mock_db_read_all, valid_department_row):
        mock_db_read_all.return_value = [valid_department_row]
        departments = get_all_departments(active_only=True)
        assert len(departments) == 1
        assert departments[0]["name"] == "Computer Science"
        mock_db_read_all.assert_called_once()

    def test_get_all_departments_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_departments(active_only=True)

    def test_get_department_by_id(self, mock_db_read_one, valid_department_row):
        mock_db_read_one.return_value = valid_department_row
        department = get_department_by_id(1)
        assert department["name"] == "Computer Science"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_department_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        department = get_department_by_id(123)
        assert department is None


class TestDepartmentCreateService:
    def test_create_new_departments(
        self,
        mock_db_create,
        mock_db_read_many,
        valid_department_create_data,
        valid_department_rows,
    ):
        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_department_rows

        results, error, status_code = create_new_departments(
            valid_department_create_data
        )

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_departments_failure(
        self, mock_db_create, mock_db_read_many, valid_department_create_data
    ):
        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_departments(
            valid_department_create_data
        )

        assert results == []
        assert error["message"] == "No departments were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


class TestDepartmentUpdateService:
    def test_update_departments(
        self,
        mock_db_update,
        mock_db_read_many,
        valid_department_update_data,
        valid_department_row,
    ):
        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_department_row]

        results, error, status_code = update_departments(valid_department_update_data)

        assert len(results) == 1
        assert error == []
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_departments_no_success(
        self, mock_db_update, mock_db_read_many, valid_department_update_data
    ):
        mock_db_update.return_value = 0
        results, error, status_code = update_departments(valid_department_update_data)

        assert results == []
        assert error == [{"message": "Department ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_departments_missing_id(
        self, mock_db_update, mock_db_read_many, department_missing_id
    ):
        results, error, status_code = update_departments(department_missing_id)

        assert results == []
        assert error == [{"message": "Missing department ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


class TestDepartmentArchiveService:
    def test_archive_departments(self, mock_db_archive, valid_department_ids):
        mock_db_archive.side_effect = [1, 1]
        archived, errors, status_code = archive_departments(valid_department_ids)

        assert len(archived) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_departments_none_archived(
        self, mock_db_archive, valid_department_ids
    ):
        mock_db_archive.return_value = 0
        archived, errors, status_code = archive_departments(valid_department_ids)

        assert archived == []

    def test_archive_departments_invalid_ids(self):
        results, errors, status = archive_departments(["one", 2])
        assert status == 400
        assert any("must be integers" in e["message"] for e in errors)



# =======================
# Model Tests
# =======================


class TestDepartmentModel:
    @patch("app.models.department.db.execute_query")
    def test_department_db_read_all(self, mock_execute):
        mock_execute.return_value = [("mocked",)]
        result = department_db_read_all()
        assert result == [("mocked",)]
        mock_execute.assert_called_once_with("SELECT * FROM departments;")

    @patch("app.models.department.db.execute_query")
    def test_department_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [("active_department",)]
        result = department_db_read_all(active_only=True)
        assert result == [("active_department",)]
        mock_execute.assert_called_once_with(
            "SELECT * FROM departments WHERE is_archived = 0;"
        )

    @patch("app.models.department.db.execute_query")
    def test_department_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [("department_1",)]
        result = department_db_read_by_id(1)
        assert result == ("department_1",)
        mock_execute.assert_called_once_with(
            "SELECT * FROM departments WHERE id = ?;", (1,)
        )

    @patch("app.models.department.db.execute_query")
    def test_department_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = department_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.department.db.execute_query")
    def test_department_db_read_by_ids_empty_list(self, mock_execute):
        result = department_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.department.db.execute_query")
    def test_department_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [("d1",), ("d2",)]
        result = department_db_read_by_ids([1, 2])

        assert result == [("d1",), ("d2",)]
        mock_execute.assert_called_once()
        assert "IN (?,?)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.department.db.execute_query")
    def test_department_db_insert_success(self, mock_execute, valid_department_row):
        mock_cursor = type("MockCursor", (), {"lastrowid": 10})()
        mock_execute.return_value = mock_cursor

        params = (valid_department_row[1],)
        result = department_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO departments" in query
        assert called_params == params

    @patch("app.models.department.db.execute_query")
    def test_department_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = department_db_insert(("bad",))
        assert result is None

    @patch("app.models.department.db.execute_query")
    def test_department_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = department_db_update(1, ("name",))
        assert result == 1

    @patch("app.models.department.db.execute_query")
    def test_department_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = department_db_update(1, ("name",))
        assert result == 0

    @patch("app.models.department.db.execute_query")
    def test_department_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = department_db_archive(1)
        assert result == 1

    @patch("app.models.department.db.execute_query")
    def test_department_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = department_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestDepartmentReadRoute:
    @patch("app.routes.department.get_all_departments")
    def test_handle_department_db_read_all_success(
        self, mock_get, client, valid_department_create_data
    ):
        mock_get.return_value = valid_department_create_data

        resp = client.get("/departments")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Departments fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_department_create_data
        mock_get.assert_called_once()

    @patch("app.routes.department.get_all_departments")
    def test_handle_department_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/departments")
        data = response.get_json()

        assert response.status_code == 500
        assert "Unexpected error: DB failure" in data["error"]
        mock_get_all.assert_called_once()

    @patch("app.routes.department.get_department_by_id")
    def test_handle_get_department_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "name": "Computer Science"}

        response = client.get("/departments/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Department fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.department.get_department_by_id")
    def test_handle_get_department_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/departments/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Department not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.department.get_department_by_id")
    def test_handle_get_department_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/departments/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "Unexpected error: DB error" in data["error"]
        mock_get_by_id.assert_called_once_with(1)


class TestDepartmentCreateRoute:
    @patch("app.routes.department.create_new_departments")
    def test_handle_department_db_insert_success(
        self, mock_create_new_departments, client, valid_department_create_data
    ):
        mock_create_new_departments.return_value = (
            valid_department_create_data,
            None,
            201,
        )

        response = client.post("/departments", json=valid_department_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 departments created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.department.create_new_departments")
    def test_handle_department_db_insert_service_error(
        self, mock_create_new_departments, client, valid_department_create_data
    ):
        error_data = [{"message": "Invalid data"}]
        error_code = 400
        mock_create_new_departments.return_value = ([], error_data, error_code)

        response = client.post("/departments", json=valid_department_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["errors"][0]["message"]

    @patch("app.routes.department.create_new_departments")
    def test_handle_department_db_insert_key_error(
        self, mock_create_new_departments, client, valid_department_create_data
    ):
        mock_create_new_departments.side_effect = KeyError("name")

        response = client.post("/departments", json=valid_department_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.department.create_new_departments")
    def test_handle_department_db_insert_exception(
        self, mock_create_new_departments, client, valid_department_create_data
    ):
        mock_create_new_departments.side_effect = Exception("DB failure")

        response = client.post("/departments", json=valid_department_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()


class TestDepartmentUpdateRoute:
    @patch("app.routes.department.update_departments")
    def test_handle_update_departments_success(
        self, mock_update_departments, client, valid_department_update_data
    ):
        mock_update_departments.return_value = (
            valid_department_update_data,
            [],
            200,
        )

        response = client.put("/departments", json=valid_department_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Department updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.department.update_departments")
    def test_handle_update_departments_service_error(
        self, mock_update_departments, client, valid_department_update_data
    ):
        error_data = [{"message": "Invalid data"}]
        error_code = 400
        mock_update_departments.return_value = ([], error_data, error_code)

        response = client.put("/departments", json=valid_department_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["errors"][0]["message"]

    @patch("app.routes.department.update_departments")
    def test_handle_update_departments_key_error(
        self, mock_update_departments, client, valid_department_update_data
    ):
        mock_update_departments.side_effect = KeyError("name")

        response = client.put("/departments", json=valid_department_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.department.update_departments")
    def test_handle_update_departments_exception(
        self, mock_update_departments, client, valid_department_update_data
    ):
        mock_update_departments.side_effect = Exception("DB failure")

        response = client.put("/departments", json=valid_department_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()


class TestDepartmentArchiveRoute:
    @patch("app.routes.department.archive_departments")
    def test_handle_archive_departments_success(
        self, mock_archive_departments, client, valid_department_ids
    ):
        mock_archive_departments.return_value = ([{"id": 1}, {"id": 2}], [], 200)

        response = client.patch("/departments", json={"ids": valid_department_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 departments archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.department.archive_departments")
    def test_handle_archive_departments_service_error(
        self, mock_archive_departments, client, valid_department_ids
    ):
        error_data = [{"message": "No departments were archived"}]
        error_code = 400
        mock_archive_departments.return_value = ([], error_data, error_code)

        response = client.patch("/departments", json={"ids": valid_department_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No departments were archived" in data["errors"][0]["message"]

    @patch("app.routes.department.archive_departments")
    def test_handle_archive_departments_key_error(
        self, mock_archive_departments, client
    ):
        response = client.patch("/departments", json={})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.department.archive_departments")
    def test_handle_archive_departments_exception(
        self, mock_archive_departments, client, valid_department_ids
    ):
        mock_archive_departments.side_effect = Exception("DB failure")

        response = client.patch("/departments", json={"ids": valid_department_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal error" in data["error"].lower()
