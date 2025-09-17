import pytest
from datetime import date
from unittest.mock import patch
from app.models import (
    course_db_read_all,
    course_db_read_by_id,
    course_db_read_by_ids,
    course_db_insert,
    course_db_update,
    course_db_archive,
)
from app.services import (
    get_all_courses,
    get_course_by_id,
    create_new_courses,
    update_courses,
    archive_courses,
)

# =======================
# Fixtures
# =======================


def make_course_row():
    today = date.today().isoformat()
    return {
        "id": 1,
        "title": "Introduction to Programming",
        "code": "COMP101",
        "term_id": 1,
        "department_id": 1,
        "created_at": today,
        "updated_at": today,
        "is_archived": False,
    }


def make_course_dict():
    return {
        "title": "Introduction to Programming",
        "code": "COMP101",
        "term_id": 1,
        "department_id": 1,
    }


@pytest.fixture
def valid_course_row():
    return make_course_row()


@pytest.fixture
def valid_course_rows():
    return [make_course_row() for _ in range(2)]


@pytest.fixture
def valid_course_create_data():
    return [
        make_course_dict(),
        {
            "title": "Data Structures",
            "code": "COMP201",
            "term_id": 1,
            "department_id": 1,
        },
    ]


@pytest.fixture
def valid_course_update_data():
    data = make_course_dict()
    data["id"] = 1
    return [data]


@pytest.fixture
def course_missing_id(valid_course_update_data):
    data = [item.copy() for item in valid_course_update_data]
    for d in data:
        d.pop("id", None)
    return data


@pytest.fixture
def valid_course_ids():
    return [1, 2]


# =======================
# DB Mock Fixtures
# =======================


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.course.course_db_read_all") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.course.course_db_read_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.course.course_db_read_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.course.course_db_insert") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.course.course_db_update") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.course.course_db_archive") as mock:
        yield mock


# =======================
# Service Tests
# =======================


class TestCourseReadService:
    def test_get_all_courses(self, mock_db_read_all, valid_course_row):
        mock_db_read_all.return_value = [valid_course_row]
        courses = get_all_courses(active_only=True)
        assert len(courses) == 1
        assert courses[0]["title"] == "Introduction to Programming"
        mock_db_read_all.assert_called_once()

    def test_get_all_courses_none(self, mock_db_read_all):
        mock_db_read_all.return_value = None
        with pytest.raises(RuntimeError):
            get_all_courses(active_only=True)

    def test_get_course_by_id(self, mock_db_read_one, valid_course_row):
        mock_db_read_one.return_value = valid_course_row
        course = get_course_by_id(1)
        assert course["title"] == "Introduction to Programming"
        mock_db_read_one.assert_called_once_with(1)

    def test_get_course_by_id_not_found(self, mock_db_read_one):
        mock_db_read_one.return_value = None
        course = get_course_by_id(123)
        assert course is None


@patch("app.models.course.db")
@patch("app.services.course.course_dict_to_row")
class TestCourseCreateService:
    def test_create_new_courses(
        self,
        mock_course_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_course_create_data,
        valid_course_rows,
    ):
        # Mock the course_dict_to_row function
        mock_course_dict_to_row.return_value = ("title", "code", 1, 1)

        mock_db_create.side_effect = [1, 2]
        mock_db_read_many.return_value = valid_course_rows

        results, error, status_code = create_new_courses(valid_course_create_data)

        assert len(results) == 2
        assert error is None
        assert status_code == 201
        assert mock_db_create.call_count == 2
        mock_db_read_many.assert_called_once_with([1, 2])

    def test_create_new_courses_failure(
        self,
        mock_course_dict_to_row,
        mock_db_instance,
        mock_db_create,
        mock_db_read_many,
        valid_course_create_data,
    ):
        # Mock the course_dict_to_row function
        mock_course_dict_to_row.return_value = ("title", "code", 1, 1)

        mock_db_create.side_effect = [None, None]
        results, error, status_code = create_new_courses(valid_course_create_data)

        assert results == []
        assert error["message"] == "No courses were created."
        assert status_code == 400
        mock_db_read_many.assert_not_called()


@patch("app.models.course.db")
@patch("app.services.course.course_dict_to_row")
class TestCourseUpdateService:
    def test_update_courses(
        self,
        mock_course_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_course_update_data,
        valid_course_row,
    ):
        # Mock the course_dict_to_row function
        mock_course_dict_to_row.return_value = ("title", "code", 1, 1)

        mock_db_read_one.return_value = valid_course_row

        mock_db_update.return_value = 1
        mock_db_read_many.return_value = [valid_course_row]

        results, error, status_code = update_courses(valid_course_update_data)

        assert len(results) == 1
        assert error in (None, [])
        assert status_code == 200
        assert mock_db_update.call_count == 1
        mock_db_read_many.assert_called_once_with([1])

    def test_update_courses_no_success(
        self,
        mock_course_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        valid_course_update_data,
        valid_course_row,
    ):
        # Mock the course_dict_to_row function
        mock_course_dict_to_row.return_value = ("title", "code", 1, 1)

        mock_db_read_one.return_value = valid_course_row

        mock_db_update.return_value = 0
        results, error, status_code = update_courses(valid_course_update_data)

        assert results == []
        assert error == [{"message": "Course ID 1 not updated."}]
        assert status_code == 400
        mock_db_update.assert_called_once()
        mock_db_read_many.assert_not_called()

    def test_update_courses_missing_id(
        self,
        mock_course_dict_to_row,
        mock_db_instance,
        mock_db_update,
        mock_db_read_many,
        mock_db_read_one,
        course_missing_id,
    ):
        results, error, status_code = update_courses(course_missing_id)

        assert results == []
        assert error == [{"message": "Missing course ID for update."}]
        assert status_code == 400
        mock_db_update.assert_not_called()
        mock_db_read_many.assert_not_called()


@patch("app.models.course.db")
class TestCourseArchiveService:
    def test_archive_courses(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_course_ids,
        valid_course_row,
    ):
        # Mock that courses exist
        mock_db_read_one.return_value = valid_course_row  # Mock get_existing_func
        mock_db_read_many.return_value = [
            valid_course_row,
            valid_course_row,
        ]  # Mock read_by_ids_func
        mock_db_archive.side_effect = [1, 1]
        archived = archive_courses(valid_course_ids)

        assert len(archived[0]) == 2
        assert mock_db_archive.call_count == 2

    def test_archive_courses_none_archived(
        self,
        mock_db_instance,
        mock_db_archive,
        mock_db_read_one,
        mock_db_read_many,
        valid_course_ids,
        valid_course_row,
    ):
        # Mock that courses exist
        mock_db_read_one.return_value = valid_course_row  # Mock get_existing_func
        mock_db_archive.return_value = 0
        archived = archive_courses(valid_course_ids)

        assert archived[0] == []

    def test_archive_courses_invalid_ids(
        self, mock_db_instance, mock_db_archive, mock_db_read_one, mock_db_read_many
    ):
        results, errors, status = archive_courses(["one", 2])
        assert status == 400
        assert any("must be of type int" in e["message"] for e in errors)


# =======================
# Model Tests
# =======================


class TestCourseModel:
    @patch("app.models.course.db.execute_query")
    def test_course_db_read_all(self, mock_execute):
        mock_execute.return_value = [{"mocked": True}]
        result = course_db_read_all()
        assert result == [{"mocked": True}]
        mock_execute.assert_called_once_with("SELECT * FROM courses;")

    @patch("app.models.course.db.execute_query")
    def test_course_db_read_all_active(self, mock_execute):
        mock_execute.return_value = [{"mocked": True}]
        result = course_db_read_all(active_only=True)
        assert result == [{"mocked": True}]
        # call contains archived condition generated by db_utils
        mock_execute.assert_called_once()

    @patch("app.models.course.db.execute_query")
    def test_course_db_read_by_id_found(self, mock_execute):
        mock_execute.return_value = [{"id": 1, "title": "x"}]
        result = course_db_read_by_id(1)
        assert result == {"id": 1, "title": "x"}
        mock_execute.assert_called_once_with(
            "SELECT * FROM courses WHERE id = %s;", (1,)
        )

    @patch("app.models.course.db.execute_query")
    def test_course_db_read_by_id_not_found(self, mock_execute):
        mock_execute.return_value = []
        result = course_db_read_by_id(999)
        assert result is None
        mock_execute.assert_called_once()

    @patch("app.models.course.db.execute_query")
    def test_course_db_read_by_ids_empty_list(self, mock_execute):
        result = course_db_read_by_ids([])
        assert result == []
        mock_execute.assert_not_called()

    @patch("app.models.course.db.execute_query")
    def test_course_db_read_by_ids_success(self, mock_execute):
        mock_execute.return_value = [{"id": 1}, {"id": 2}]
        result = course_db_read_by_ids([1, 2])

        assert result == [{"id": 1}, {"id": 2}]
        mock_execute.assert_called_once()
        assert "IN (%s,%s)" in mock_execute.call_args.args[0]
        assert mock_execute.call_args.args[1] == [1, 2]

    @patch("app.models.course.db.execute_query")
    def test_course_db_insert_success(self, mock_execute, valid_course_row):
        # PostgreSQL RETURNING result (list of dicts)
        mock_execute.return_value = [{"id": 10}]

        params = (
            valid_course_row["title"],
            valid_course_row["code"],
            valid_course_row["term_id"],
            valid_course_row["department_id"],
        )
        result = course_db_insert(params)

        assert result == 10
        mock_execute.assert_called_once()

        query, called_params = mock_execute.call_args.args
        assert "INSERT INTO courses" in query
        assert called_params == params

    @patch("app.models.course.db.execute_query")
    def test_course_db_insert_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_db_insert(("bad",))
        assert result is None

    @patch("app.models.course.db.execute_query")
    def test_course_db_update_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor

        result = course_db_update(1, ("x",) * 4)
        assert result == 1

    @patch("app.models.course.db.execute_query")
    def test_course_db_update_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_db_update(1, ("x",) * 4)
        assert result == 0

    @patch("app.models.course.db.execute_query")
    def test_course_db_archive_success(self, mock_execute):
        mock_cursor = type("MockCursor", (), {"rowcount": 1})()
        mock_execute.return_value = mock_cursor
        result = course_db_archive(1)
        assert result == 1

    @patch("app.models.course.db.execute_query")
    def test_course_db_archive_failure(self, mock_execute):
        mock_execute.return_value = None
        result = course_db_archive(999)
        assert result == 0


# =======================
# Route Tests
# =======================


class TestCourseReadRoute:
    @patch("app.routes.course.get_all_courses")
    def test_handle_course_db_read_all_success(
        self, mock_get, client, valid_course_create_data
    ):
        mock_get.return_value = valid_course_create_data

        resp = client.get("/courses")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "Courses fetched successfully." in data["message"]
        assert isinstance(data["data"], list)
        assert data["data"] == valid_course_create_data
        mock_get.assert_called_once()

    @patch("app.routes.course.get_all_courses")
    def test_handle_course_db_read_all_exception(self, mock_get_all, client):
        mock_get_all.side_effect = Exception("DB failure")

        response = client.get("/courses")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
        mock_get_all.assert_called_once()

    @patch("app.routes.course.get_course_by_id")
    def test_handle_get_course_by_id_success(self, mock_get_by_id, client):
        mock_get_by_id.return_value = {"id": 1, "title": "Introduction to Programming"}

        response = client.get("/courses/1")
        data = response.get_json()

        assert response.status_code == 200
        assert "Course fetched successfully" in data["message"]
        assert data["data"]["id"] == 1
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.routes.course.get_course_by_id")
    def test_handle_get_course_by_id_not_found(self, mock_get_by_id, client):
        mock_get_by_id.return_value = None

        response = client.get("/courses/999")
        data = response.get_json()

        assert response.status_code == 404
        assert "Course not found" in data["error"]
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.routes.course.get_course_by_id")
    def test_handle_get_course_by_id_exception(self, mock_get_by_id, client):
        mock_get_by_id.side_effect = Exception("DB error")

        response = client.get("/courses/1")
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db error" in data["error"].lower()
        mock_get_by_id.assert_called_once_with(1)


class TestCourseCreateRoute:
    @patch("app.routes.course.create_new_courses")
    def test_handle_course_db_insert_success(
        self, mock_create_new_courses, client, valid_course_create_data
    ):
        mock_create_new_courses.return_value = (valid_course_create_data, None, None)

        response = client.post("/courses", json=valid_course_create_data)
        data = response.get_json()

        assert response.status_code == 201
        assert "2 courses created successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course.create_new_courses")
    def test_handle_course_db_insert_service_error(
        self, mock_create_new_courses, client, valid_course_create_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 400
        mock_create_new_courses.return_value = ([], error_data, error_code)

        response = client.post("/courses", json=valid_course_create_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.course.create_new_courses")
    def test_handle_course_db_insert_key_error(
        self, mock_create_new_courses, client, valid_course_create_data
    ):
        mock_create_new_courses.side_effect = KeyError("title")

        response = client.post("/courses", json=valid_course_create_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course.create_new_courses")
    def test_handle_course_db_insert_exception(
        self, mock_create_new_courses, client, valid_course_create_data
    ):
        mock_create_new_courses.side_effect = Exception("DB failure")

        response = client.post("/courses", json=valid_course_create_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestCourseUpdateRoute:
    @patch("app.routes.course.update_courses")
    def test_handle_update_courses_success(
        self, mock_update_courses, client, valid_course_update_data
    ):
        mock_update_courses.return_value = (valid_course_update_data, None, None)

        response = client.put("/courses", json=valid_course_update_data)
        data = response.get_json()

        assert response.status_code == 200
        assert "Course updated successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course.update_courses")
    def test_handle_update_courses_service_error(
        self, mock_update_courses, client, valid_course_update_data
    ):
        error_data = {"message": "Invalid data"}
        error_code = 422
        mock_update_courses.return_value = ([], error_data, error_code)

        response = client.put("/courses", json=valid_course_update_data)
        data = response.get_json()

        assert response.status_code == error_code
        assert "Invalid data" in data["message"]

    @patch("app.routes.course.update_courses")
    def test_handle_update_courses_key_error(
        self, mock_update_courses, client, valid_course_update_data
    ):
        mock_update_courses.side_effect = KeyError("title")

        response = client.put("/courses", json=valid_course_update_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course.update_courses")
    def test_handle_update_courses_exception(
        self, mock_update_courses, client, valid_course_update_data
    ):
        mock_update_courses.side_effect = Exception("DB failure")

        response = client.put("/courses", json=valid_course_update_data)
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()


class TestCourseArchiveRoute:
    @patch("app.routes.course.archive_courses")
    def test_handle_archive_courses_success(
        self, mock_archive_courses, client, valid_course_ids
    ):
        mock_archive_courses.return_value = (valid_course_ids, None, 200)

        response = client.patch("/courses", json={"ids": valid_course_ids})
        data = response.get_json()

        assert response.status_code == 200
        assert "2 courses archived successfully" in data["message"]
        assert data["data"]

    @patch("app.routes.course.archive_courses")
    def test_handle_archive_courses_service_error(
        self, mock_archive_courses, client, valid_course_ids
    ):
        error_data = {"message": "No courses were archived."}
        error_code = 400
        mock_archive_courses.return_value = ([], error_data, error_code)

        response = client.patch("/courses", json={"ids": valid_course_ids})
        data = response.get_json()

        assert response.status_code == error_code
        assert "No courses were archived." in data["message"]

    @patch("app.routes.course.archive_courses")
    def test_handle_archive_courses_key_error(
        self, mock_archive_courses, client, valid_course_ids
    ):
        mock_archive_courses.side_effect = KeyError("ids")

        response = client.patch("/courses", json={"ids": valid_course_ids})
        data = response.get_json()

        assert response.status_code == 400
        assert "Missing required field" in data["error"]

    @patch("app.routes.course.archive_courses")
    def test_handle_archive_courses_exception(
        self, mock_archive_courses, client, valid_course_ids
    ):
        mock_archive_courses.side_effect = Exception("DB failure")

        response = client.patch("/courses", json={"ids": valid_course_ids})
        data = response.get_json()

        assert response.status_code == 500
        assert "internal server error: db failure." in data["error"].lower()
