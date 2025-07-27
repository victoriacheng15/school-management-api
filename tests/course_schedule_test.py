import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    course_schedule_db_read_all,
    course_schedule_db_read_by_id,
    course_schedule_db_read_by_ids,
    course_schedule_db_insert,
    course_schedule_db_update,
    course_schedule_db_archive,
)
from app.services import (
    get_all_course_schedules,
    get_course_schedule_by_id,
    create_new_course_schedules,
    update_course_schedules,
    archive_course_schedules,
)

# =======================
# Fixtures
# =======================


def make_course_schedule_row():
    today = date.today().isoformat()
    return (
        1,
        1,
        "Monday",
        "10:00",
        "Room 101",
        today,
        today,
        0,
    )


def make_course_schedule_dict():
    return {
        "course_id": 1,
        "day": "Monday",
        "time": "10:00",
        "room": "Room 101",
    }


@pytest.fixture
def valid_course_schedule_row():
    return make_course_schedule_row()


@pytest.fixture
def valid_course_schedule_rows():
    return [make_course_schedule_row() for _ in range(2)]


@pytest.fixture
def valid_course_schedule_create_data():
    return [
        make_course_schedule_dict(),
        {
            "course_id": 2,
            "day": "Tuesday",
            "time": "11:00",
            "room": "Room 102",
        },
    ]


@pytest.fixture
def valid_course_schedule_update_data():
    data = make_course_schedule_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def course_schedule_missing_id(valid_course_schedule_update_data):
    data = [item.copy() for item in valid_course_schedule_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_course_schedule_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.course_schedule.course_schedule_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.course_schedule.course_schedule_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.course_schedule.course_schedule_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.course_schedule.course_schedule_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.course_schedule.course_schedule_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.course_schedule.course_schedule_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestCourseScheduleReadService:
    def test_get_all_course_schedules(
        self, mock_db_read_all, valid_course_schedule_row
    ):
        mock_db_read_all.return_value = [valid_course_schedule_row]
        course_schedules = get_all_course_schedules(active_only=True)
        assert len(course_schedules) == 1
        assert course_schedules[0]["day"] == "Monday"
        mock_db_read_all.assert_called_once()

    def test_get_all_course_schedules_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_course_schedules(active_only=True)

    def test_get_course_schedule_by_id(
        self, mock_db_read_one, valid_course_schedule_row
    ):
        mock_db_read_one.return_value = valid_course_schedule_row
        course_schedule = get_course_schedule_by_id(1)
        assert course_schedule["day"] == "Monday"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_course_schedule_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        course_schedule = get_course_schedule_by_id(123)
        assert course_schedule is None


class TestCourseScheduleCreateService:
    def test_create_new_course_schedules(
        self,
        mock_db_create,
        mock_db_read_many,
        valid_course_schedule_create_data,
        valid_course_schedule_rows,
    ):
        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_course_schedule_rows

        results, error, status_code = create_new_course_schedules(
            valid_course_schedule_create_data
        )

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_course_schedules_failure(
        self, mock_db_create, mock_db_read_many, valid_course_schedule_create_data
    ):
        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_course_schedules(
            valid_course_schedule_create_data
        )

        assert results == []
        assert error["message"] == "No course schedules were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


class TestCourseScheduleUpdateService:
    def test_update_course_schedules(
        self,
        mock_db_update,
        mock_db_read_many,
        valid_course_schedule_update_data,
        valid_course_schedule_row,
    ):
        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_course_schedule_row]

        results, error, status_code = update_course_schedules(
            valid_course_schedule_update_data
        )

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_course_schedules_no_success(
        self, mock_db_update, mock_db_read_many, valid_course_schedule_update_data
    ):
        mock_db_update.return_value = 0
        results, error, status_code = update_course_schedules(
            valid_course_schedule_update_data
        )

        assert results == []
        assert error == [{"message": "Course schedule ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_course_schedules_missing_id(
        self, mock_db_update, mock_db_read_many, course_schedule_missing_id
    ):
        results, error, status_code = update_course_schedules(
            course_schedule_missing_id
        )

        assert results == []
        assert error == [{"message": "Missing course schedule ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


class TestCourseScheduleArchiveService:
    def test_archive_course_schedules(self, mock_db_archive, valid_course_schedule_ids):
        mock_db_archive.side_effect = [1, 1]
        archived = archive_course_schedules(valid_course_schedule_ids)

        assert len(archived[0]) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_course_schedules_none_archived(
        self, mock_db_archive, valid_course_schedule_ids
    ):
        mock_db_archive.return_value = 0
        archived = archive_course_schedules(valid_course_schedule_ids)

        assert archived[0] == []

    def test_archive_course_schedules_invalid_ids(self):
        results, errors, status = archive_course_schedules(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestCourseScheduleModel:
    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_all(self, mock_execute):
        mock_execute.return_value = [("mocked",)]
        result = course_schedule_db_read_all()
        assert result == [("mocked",)]
        mock_execute.assert_called_once_with("SELECT * FROM course_schedule;")

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [("active_course_schedule",)]
        result = course_schedule_db_read_all(active_only=True)
        assert result == [("active_course_schedule",)]
        mock_execute.assert_called_once_with(
            "SELECT * FROM course_schedule WHERE is_archived = 0;"
        )

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [("course_schedule_1",)]
        result = course_schedule_db_read_by_id(1)
        assert result == ("course_schedule_1",)
        mock_execute.assert_called_once_with(
            "SELECT * FROM course_schedule WHERE id = ?;", (1,)
        )

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = course_schedule_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_by_ids_empty_list(self, mock_execute):
        result = course_schedule_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [("cs1",), ("cs2",)]
        result = course_schedule_db_read_by_ids([1, 2])

        assert result == [("cs1",), ("cs2",)]
        mock_execute.assert_called_once()
        assert "IN (?,?)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_insert_success(
        self, mock_execute, valid_course_schedule_row
    ):
        mock_cursor = type("MockCursor", (), {"lastrowid": 10})()
        mock_execute.return_value = mock_cursor

        params = valid_course_schedule_row[
            1:5
        ]  # Exclude id, created_at, updated_at, is_archived
        result = course_schedule_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO course_schedule" in query
        assert called_params == params

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_schedule_db_insert(("bad",))
        assert result is None

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = course_schedule_db_update(1, ("x",) * 4)  # course_id, day, time, room
        assert result == 1

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_schedule_db_update(1, ("x",) * 4)
        assert result == 0

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = course_schedule_db_archive(1)
        assert result == 1

    @patch("app.models.course_schedule.db.execute_query")
    def test_course_schedule_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_schedule_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestCourseScheduleReadRoute:
    @patch("app.routes.course_schedule.get_all_course_schedules")
    def test_handle_course_schedule_db_read_all_success(
        self, mock_get, client, valid_course_schedule_create_data
    ):
        mock_get.return_value = valid_course_schedule_create_data

        resp = client.get("/course_schedules")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Course schedules fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_course_schedule_create_data
        mock_get.assert_called_once()

    @patch("app.routes.course_schedule.get_all_course_schedules")
    def test_handle_course_schedule_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/course_schedules")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.course_schedule.get_course_schedule_by_id")
    def test_handle_get_course_schedule_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "day": "Monday"}

        response = client.get("/course_schedules/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Course schedule fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.course_schedule.get_course_schedule_by_id")
    def test_handle_get_course_schedule_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/course_schedules/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Course schedule not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.course_schedule.get_course_schedule_by_id")
    def test_handle_get_course_schedule_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/course_schedules/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestCourseScheduleCreateRoute:
    @patch("app.routes.course_schedule.create_new_course_schedules")
    def test_handle_course_schedule_db_insert_success(
        self,
        mock_create_new_course_schedules,
        client,
        valid_course_schedule_create_data,
    ):
        mock_create_new_course_schedules.return_value = (
            valid_course_schedule_create_data,
            None,
            None,
        )

        response = client.post(
            "/course_schedules", json=valid_course_schedule_create_data
        )
        data = response.get_json()

        assert response.status_code == 201
        assert "2 course schedules created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course_schedule.create_new_course_schedules")
    def test_handle_course_schedule_db_insert_service_error(
        self,
        mock_create_new_course_schedules,
        client,
        valid_course_schedule_create_data,
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_course_schedules.return_value = ([], error_data, error_code)

        response = client.post(
            "/course_schedules", json=valid_course_schedule_create_data
        )
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.course_schedule.create_new_course_schedules")
    def test_handle_course_schedule_db_insert_key_error(
        self,
        mock_create_new_course_schedules,
        client,
        valid_course_schedule_create_data,
    ):
        mock_create_new_course_schedules.side_effect = KeyError("course_id")

        response = client.post(
            "/course_schedules", json=valid_course_schedule_create_data
        )
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course_schedule.create_new_course_schedules")
    def test_handle_course_schedule_db_insert_exception(
        self,
        mock_create_new_course_schedules,
        client,
        valid_course_schedule_create_data,
    ):
        mock_create_new_course_schedules.side_effect = Exception("DB failure")

        response = client.post(
            "/course_schedules", json=valid_course_schedule_create_data
        )
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestCourseScheduleUpdateRoute:
    @patch("app.routes.course_schedule.update_course_schedules")
    def test_handle_update_course_schedules_success(
        self, mock_update_course_schedules, client, valid_course_schedule_update_data
    ):
        mock_update_course_schedules.return_value = (
            valid_course_schedule_update_data,
            None,
            None,
        )

        response = client.put(
            "/course_schedules", json=valid_course_schedule_update_data
        )
        data = response.get_json()

        assert response.status_code == 200
        assert "Course schedule updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course_schedule.update_course_schedules")
    def test_handle_update_course_schedules_service_error(
        self, mock_update_course_schedules, client, valid_course_schedule_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_course_schedules.return_value = ([], error_data, error_code)

        response = client.put(
            "/course_schedules", json=valid_course_schedule_update_data
        )
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.course_schedule.update_course_schedules")
    def test_handle_update_course_schedules_key_error(
        self, mock_update_course_schedules, client, valid_course_schedule_update_data
    ):
        mock_update_course_schedules.side_effect = KeyError("course_id")

        response = client.put(
            "/course_schedules", json=valid_course_schedule_update_data
        )
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course_schedule.update_course_schedules")
    def test_handle_update_course_schedules_exception(
        self, mock_update_course_schedules, client, valid_course_schedule_update_data
    ):
        mock_update_course_schedules.side_effect = Exception("DB failure")

        response = client.put(
            "/course_schedules", json=valid_course_schedule_update_data
        )
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestCourseScheduleArchiveRoute:
    @patch("app.routes.course_schedule.archive_course_schedules")
    def test_handle_archive_course_schedules_success(
        self, mock_archive_course_schedules, client, valid_course_schedule_ids
    ):
        mock_archive_course_schedules.return_value = (
            valid_course_schedule_ids,
            None,
            200,
        )

        response = client.patch(
            "/course_schedules", json={"ids": valid_course_schedule_ids}
        )
        data = response.get_json()

        assert response.status_code == 200
        assert "2 course schedules archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course_schedule.archive_course_schedules")
    def test_handle_archive_course_schedules_service_error(
        self, mock_archive_course_schedules, client, valid_course_schedule_ids
    ):
        error_data = {"message": "No course schedules were archived."}
        error_code = 400
        mock_archive_course_schedules.return_value = ([], error_data, error_code)

        response = client.patch(
            "/course_schedules", json={"ids": valid_course_schedule_ids}
        )
        data = response.get_json()

        assert response.status_code == error_code
        assert "No course schedules were archived." in data["message"]

    @patch("app.routes.course_schedule.archive_course_schedules")
    def test_handle_archive_course_schedules_key_error(
        self, mock_archive_course_schedules, client, valid_course_schedule_ids
    ):
        mock_archive_course_schedules.side_effect = KeyError("ids")

        response = client.patch(
            "/course_schedules", json={"ids": valid_course_schedule_ids}
        )
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course_schedule.archive_course_schedules")
    def test_handle_archive_course_schedules_exception(
        self, mock_archive_course_schedules, client, valid_course_schedule_ids
    ):
        mock_archive_course_schedules.side_effect = Exception("DB failure")

        response = client.patch(
            "/course_schedules", json={"ids": valid_course_schedule_ids}
        )
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
