import pytest
from unittest.mock import patch
from app.services.student import (
    get_all_active_students,
    get_student_by_id,
    create_students,
    update_students,
    archive_students,
)


@pytest.fixture
def mock_db_read_all():
    with patch("app.services.student.read_all_active_students") as mock:
        yield mock


@pytest.fixture
def mock_db_read_one():
    with patch("app.services.student.read_student_by_id") as mock:
        yield mock


@pytest.fixture
def mock_db_read_many():
    with patch("app.services.student.read_students_by_ids") as mock:
        yield mock


@pytest.fixture
def mock_db_create():
    with patch("app.services.student.create_student") as mock:
        yield mock


@pytest.fixture
def mock_db_update():
    with patch("app.services.student.update_student") as mock:
        yield mock


@pytest.fixture
def mock_db_archive():
    with patch("app.services.student.archive_student") as mock:
        yield mock


def test_get_all_active_students(mock_db_read_all):
    mock_db_read_all.return_value = [
        (1, "John", "Doe", "a@a.com", "123 Main St", "Anytown", "ON", "Canada", "local", "active", 0, 0, 1, "2024-01-01", "2024-01-01", 0)
    ]
    students = get_all_active_students()
    assert len(students) == 1
    assert students[0]["first_name"] == "John"
    mock_db_read_all.assert_called_once()


def test_get_student_by_id(mock_db_read_one):
    mock_db_read_one.return_value = (1, "John", "Doe", "a@a.com", "123 Main St", "Anytown", "ON", "Canada", "local", "active", 0, 0, 1, "2024-01-01", "2024-01-01", 0)
    student = get_student_by_id(1)
    assert student["first_name"] == "John"
    mock_db_read_one.assert_called_once_with(1)


def test_create_students(mock_db_create, mock_db_read_many):
    student_data = [
        {"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "is_international": False},
        {"first_name": "Jane", "last_name": "Doe", "email": "janedoe@example.com", "is_international": True},
    ]
    mock_db_create.side_effect = [1, 2]
    mock_db_read_many.return_value = [
        (1, "John", "Doe", "johndoe@example.com", None, None, None, None, "local", "active", 0, False, None, "2024-07-12", "2024-07-12", 0),
        (2, "Jane", "Doe", "janedoe@example.com", None, None, None, None, "local", "active", 0, True, None, "2024-07-12", "2024-07-12", 0),
    ]

    created_students, error = create_students(student_data)

    assert error is None
    assert len(created_students) == 2
    assert mock_db_create.call_count == 2
    mock_db_read_many.assert_called_once_with([1, 2])


def test_update_students(mock_db_update, mock_db_read_many):
    student_data = [
        {"id": 1, "first_name": "John", "last_name": "Doe", "email": "johndoe@example.com", "is_international": False},
    ]
    mock_db_update.return_value = 1
    mock_db_read_many.return_value = [
        (1, "John", "Doe", "johndoe@example.com", None, None, None, None, "local", "active", 0, False, None, "2024-07-12", "2024-07-12", 0),
    ]

    updated_students, error = update_students(student_data)

    assert error is None
    assert len(updated_students) == 1
    assert mock_db_update.call_count == 1
    mock_db_read_many.assert_called_once_with([1])


def test_archive_students(mock_db_archive):
    student_ids = [1, 2]
    mock_db_archive.side_effect = [1, 1]

    archived_ids = archive_students(student_ids)

    assert len(archived_ids) == 2
    assert mock_db_archive.call_count == 2