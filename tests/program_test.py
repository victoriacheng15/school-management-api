import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    program_db_read_all,
    program_db_read_by_id,
    program_db_read_by_ids,
    program_db_insert,
    program_db_update,
    program_db_archive,
)
from app.services import (
    get_all_programs,
    get_program_by_id,
    create_new_programs,
    update_programs,
    archive_programs,
)

# =======================
# Fixtures
# =======================


def make_program_row():
    today = date.today().isoformat()
    return {
        "id": 1,
        "name": "Computer Science",
        "type": "bachelor",
        "department_id": 1,
        "created_at": today,
        "updated_at": today,
        "is_archived": False,
    }


def make_program_dict():
    return {
        "name": "Computer Science",
        "type": "bachelor",
        "department_id": 1,
    }


@pytest.fixture
def valid_program_row():
    return make_program_row()


@pytest.fixture
def valid_program_rows():
    return [make_program_row() for _ in range(2)]


@pytest.fixture
def valid_program_create_data():
    return [
        make_program_dict(),
        {
            "name": "Software Engineering",
            "type": "bachelor",
            "department_id": 1,
        },
    ]


@pytest.fixture
def valid_program_update_data():
    data = make_program_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def program_missing_id(valid_program_update_data):
    data = [item.copy() for item in valid_program_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_program_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.program.program_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.program.program_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.program.program_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.program.program_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.program.program_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.program.program_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestProgramReadService:
    def test_get_all_programs(self, mock_db_read_all, valid_program_row):
        mock_db_read_all.return_value = [valid_program_row]

        programs = get_all_programs(active_only=True)
        assert len(programs) == 1
        assert programs[0]["name"] == "Computer Science"
        mock_db_read_all.assert_called_once()

    def test_get_all_programs_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_programs(active_only=True)

    def test_get_program_by_id(self, mock_db_read_one, valid_program_row):
        mock_db_read_one.return_value = valid_program_row

        program = get_program_by_id(1)
        assert program["name"] == "Computer Science"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_program_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        program = get_program_by_id(123)
        assert program is None


@patch("app.models.program.db")
@patch("app.services.program.program_dict_to_row")
class TestProgramCreateService:
    def test_create_new_programs(
        self,
        mock_program_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_program_create_data,
        valid_program_rows,
    ):
        # Mock the program_dict_to_row function
        mock_program_dict_to_row.return_value = ("Computer Science", "bachelor", 1)

        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_program_rows

        results, error, status_code = create_new_programs(valid_program_create_data)

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_programs_failure(
        self,
        mock_program_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_program_create_data,
    ):
        # Mock the program_dict_to_row function
        mock_program_dict_to_row.return_value = ("Computer Science", "bachelor", 1)

        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_programs(valid_program_create_data)

        assert results == []
        assert error["message"] == "No programs were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


@patch("app.models.program.db")
@patch("app.services.program.program_dict_to_row")
class TestProgramUpdateService:
    def test_update_programs(
        self,
        mock_program_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_one,
        mock_db_read_many,
        valid_program_update_data,
        valid_program_row,
    ):
        # Mock the program_dict_to_row function
        mock_program_dict_to_row.return_value = ("Computer Science", "bachelor", 1)

        mock_db_read_one.return_value = valid_program_row

        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_program_row]

        results, error, status_code = update_programs(valid_program_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_programs_no_success(
        self,
        mock_program_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_one,
        mock_db_read_many,
        valid_program_update_data,
        valid_program_row,
    ):
        # Mock the program_dict_to_row function
        mock_program_dict_to_row.return_value = ("Computer Science", "bachelor", 1)

        mock_db_read_one.return_value = valid_program_row

        mock_db_update.return_value = 0
        results, error, status_code = update_programs(valid_program_update_data)

        assert results == []
        assert error == [{"message": "Program ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_programs_missing_id(
        self,
        mock_program_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_one,
        mock_db_read_many,
        program_missing_id,
    ):
        results, error, status_code = update_programs(program_missing_id)

        assert results == []
        assert error == [{"message": "Missing program ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


@patch("app.models.program.db")
class TestProgramArchiveService:
    def test_archive_programs(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_program_ids,
        valid_program_rows,
    ):
        mock_db_archive.side_effect = [1, 1]
        mock_db_read_one.side_effect = valid_program_rows
        mock_db_read_many.return_value = valid_program_rows
        results, errors, status = archive_programs(valid_program_ids)

        assert len(results) == 2
        assert errors in (None, [])
        assert status == 200
        assert mock_db_archive.call_count == 2

    def test_archive_programs_none_archived(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_program_ids,
        valid_program_row,
    ):
        mock_db_read_one.return_value = valid_program_row

        mock_db_archive.return_value = 0
        results, errors, status = archive_programs(valid_program_ids)

        assert results == []
        assert len(errors) == 2

    def test_archive_programs_invalid_ids(
        self, mock_db_instance, mock_db_archive, mock_db_read_one, mock_db_read_many
    ):
        results, errors, status = archive_programs(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestProgramModel:
    @patch("app.models.program.db.execute_query")
    def test_program_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": "data"}]
        result = program_db_read_all()
        assert result == [{"mocked": "data"}]
        mock_execute.assert_called_once_with("SELECT * FROM programs;")

    @patch("app.models.program.db.execute_query")
    def test_program_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [{"active": "program"}]
        result = program_db_read_all(active_only=True)
        assert result == [{"active": "program"}]
        mock_execute.assert_called_once()

    @patch("app.models.program.db.execute_query")
    def test_program_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"id": 1, "name": "Program1"}]
        result = program_db_read_by_id(1)
        assert result == {"id": 1, "name": "Program1"}
        mock_execute.assert_called_once_with(
            "SELECT * FROM programs WHERE id = %s;", (1,)
        )

    @patch("app.models.program.db.execute_query")
    def test_program_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = program_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.program.db.execute_query")
    def test_program_db_read_by_ids_empty_list(self, mock_execute):
        result = program_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.program.db.execute_query")
    def test_program_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"id": 1}, {"id": 2}]
        result = program_db_read_by_ids([1, 2])

        assert result == [{"id": 1}, {"id": 2}]
        mock_execute.assert_called_once()
        assert "IN (%s,%s)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.program.db.execute_query")
    def test_program_db_insert_success(self, mock_execute, valid_program_row):
        mock_execute.return_value = [{"id": 10}]
        params = (
            valid_program_row["name"],
            valid_program_row["type"],
            valid_program_row["department_id"],
        )

        result = program_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO programs" in query
        assert called_params == params

    @patch("app.models.program.db.execute_query")
    def test_program_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = program_db_insert(("bad",))
        assert result is None

    @patch("app.models.program.db.execute_query")
    def test_program_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = program_db_update(1, ("x",) * 3)
        assert result == 1

    @patch("app.models.program.db.execute_query")
    def test_program_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = program_db_update(1, ("x",) * 3)
        assert result == 0

    @patch("app.models.program.db.execute_query")
    def test_program_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = program_db_archive(1)
        assert result == 1

    @patch("app.models.program.db.execute_query")
    def test_program_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = program_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestProgramReadRoute:
    @patch("app.routes.program.get_all_programs")
    def test_handle_program_db_read_all_success(
        self, mock_get, client, valid_program_create_data
    ):
        mock_get.return_value = valid_program_create_data

        resp = client.get("/programs")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Programs fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_program_create_data
        mock_get.assert_called_once()

    @patch("app.routes.program.get_all_programs")
    def test_handle_program_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/programs")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.program.get_program_by_id")
    def test_handle_get_program_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "name": "Computer Science"}

        response = client.get("/programs/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Program fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.program.get_program_by_id")
    def test_handle_get_program_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/programs/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Program not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.program.get_program_by_id")
    def test_handle_get_program_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/programs/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestProgramCreateRoute:
    @patch("app.routes.program.create_new_programs")
    def test_handle_program_db_insert_success(
        self, mock_create_new_programs, client, valid_program_create_data
    ):
        mock_create_new_programs.return_value = (valid_program_create_data, None, 201)

        response = client.post("/programs", json=valid_program_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 programs created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.program.create_new_programs")
    def test_handle_program_db_insert_service_error(
        self, mock_create_new_programs, client, valid_program_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_programs.return_value = ([], error_data, error_code)

        response = client.post("/programs", json=valid_program_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.program.create_new_programs")
    def test_handle_program_db_insert_key_error(
        self, mock_create_new_programs, client, valid_program_create_data
    ):
        mock_create_new_programs.side_effect = KeyError("name")

        response = client.post("/programs", json=valid_program_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.program.create_new_programs")
    def test_handle_program_db_insert_exception(
        self, mock_create_new_programs, client, valid_program_create_data
    ):
        mock_create_new_programs.side_effect = Exception("DB failure")

        response = client.post("/programs", json=valid_program_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestProgramUpdateRoute:
    @patch("app.routes.program.update_programs")
    def test_handle_update_programs_success(
        self, mock_update_programs, client, valid_program_update_data
    ):
        mock_update_programs.return_value = (valid_program_update_data, None, 200)

        response = client.put("/programs", json=valid_program_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Program updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.program.update_programs")
    def test_handle_update_programs_service_error(
        self, mock_update_programs, client, valid_program_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_programs.return_value = ([], error_data, error_code)

        response = client.put("/programs", json=valid_program_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.program.update_programs")
    def test_handle_update_programs_key_error(
        self, mock_update_programs, client, valid_program_update_data
    ):
        mock_update_programs.side_effect = KeyError("name")

        response = client.put("/programs", json=valid_program_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.program.update_programs")
    def test_handle_update_programs_exception(
        self, mock_update_programs, client, valid_program_update_data
    ):
        mock_update_programs.side_effect = Exception("DB failure")

        response = client.put("/programs", json=valid_program_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestProgramArchiveRoute:
    @patch("app.routes.program.archive_programs")
    def test_handle_archive_programs_success(
        self, mock_archive_programs, client, valid_program_ids
    ):
        mock_archive_programs.return_value = (valid_program_ids, None, 200)

        response = client.patch("/programs", json={"ids": valid_program_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 programs archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.program.archive_programs")
    def test_handle_archive_programs_service_error(
        self, mock_archive_programs, client, valid_program_ids
    ):
        error_data = {"message": "No programs were archived."}
        error_code = 400
        mock_archive_programs.return_value = ([], error_data, error_code)

        response = client.patch("/programs", json={"ids": valid_program_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No programs were archived." in data["message"]

    @patch("app.routes.program.archive_programs")
    def test_handle_archive_programs_key_error(
        self, mock_archive_programs, client, valid_program_ids
    ):
        mock_archive_programs.side_effect = KeyError("ids")

        response = client.patch("/programs", json={"ids": valid_program_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.program.archive_programs")
    def test_handle_archive_programs_exception(
        self, mock_archive_programs, client, valid_program_ids
    ):
        mock_archive_programs.side_effect = Exception("DB failure")

        response = client.patch("/programs", json={"ids": valid_program_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
