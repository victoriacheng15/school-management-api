import pytest
import json
from unittest.mock import patch


@pytest.fixture
def single_student_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "address": "123 Main St",
        "city": "Anytown",
        "province": "ON",
        "country": "Canada",
        "address_type": "home",
        "status": "active",
        "coop": True,
        "is_international": False,
        "program_id": 1,
    }


@pytest.fixture
def bulk_students_data(single_student_data):
    return [
        single_student_data,
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "address": "456 Side St",
            "city": "Othertown",
            "province": "BC",
            "country": "Canada",
            "address_type": "home",
            "status": "active",
            "coop": False,
            "is_international": True,
            "program_id": 2,
        },
    ]


@pytest.fixture
def make_student_api_response():
    """Factory fixture to create a standardized student dictionary for API responses."""

    def _make(
        data: dict,
        id=1,
        created_at="2025-07-01 00:00:00",
        updated_at="2025-07-01 00:00:00",
        is_archived=False,
    ):
        response_data = data.copy()
        response_data.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "is_archived": is_archived,
            }
        )
        return response_data

    return _make


@pytest.mark.parametrize("is_bulk", [False, True])
@patch("app.routes.student.create_students")
def test_create_student(
    mock_create_students,
    client,
    is_bulk,
    single_student_data,
    bulk_students_data,
    make_student_api_response,
):
    # Arrange
    payload = bulk_students_data if is_bulk else single_student_data
    
    if is_bulk:
        expected_data = [
            make_student_api_response(bulk_students_data[0], id=1),
            make_student_api_response(bulk_students_data[1], id=2),
        ]
    else:
        expected_data = [make_student_api_response(single_student_data, id=1)]
    mock_create_students.return_value = (expected_data, None)

    # Act
    response = client.post(
        "/students", data=json.dumps(payload), content_type="application/json"
    )

    # Assert
    assert response.status_code == 201
    mock_create_students.assert_called_once_with(payload)
    response_data = json.loads(response.data)

    if is_bulk:
        assert "students created successfully" in response_data["message"]
        assert response_data["data"] == expected_data
    else:
        assert response_data["message"] == "Student created successfully"
        assert response_data["data"] == expected_data[0]


def test_create_student_missing_field(client, single_student_data):
    # Arrange
    payload = single_student_data.copy()
    del payload["first_name"]

    # Act
    response = client.post(
        "/students", data=json.dumps(payload), content_type="application/json"
    )

    # Assert
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert "Missing required field" in response_data["error"]
    assert "'first_name'" in response_data["error"]


@patch("app.routes.student.get_all_active_students")
def test_read_all_active_students(
    mock_get_all_active_students,
    client,
    bulk_students_data,
    make_student_api_response,
):
    # Arrange
    expected_students = [
        make_student_api_response(bulk_students_data[0], id=1),
        make_student_api_response(bulk_students_data[1], id=2),
    ]
    mock_get_all_active_students.return_value = expected_students

    # Act
    response = client.get("/students")

    # Assert
    assert response.status_code == 200
    mock_get_all_active_students.assert_called_once()
    response_data = json.loads(response.data)
    assert response_data == {
        "message": "Students fetched successfully",
        "data": expected_students,
    }


@patch("app.routes.student.get_student_by_id")
def test_read_student_by_id(
    mock_get_student_by_id, client, single_student_data, make_student_api_response
):
    # Arrange
    expected_student = make_student_api_response(single_student_data, id=1)
    mock_get_student_by_id.return_value = expected_student

    # Act
    response = client.get("/students/1")

    # Assert
    assert response.status_code == 200
    mock_get_student_by_id.assert_called_once_with(1)
    response_data = json.loads(response.data)
    assert response_data == {
        "message": "Student fetched successfully",
        "data": expected_student,
    }


@patch("app.routes.student.get_student_by_id")
def test_read_student_by_id_not_found(mock_get_student_by_id, client):
    mock_get_student_by_id.return_value = None

    response = client.get("/students/999")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "Student not found"


@pytest.mark.parametrize("is_bulk", [False, True])
@patch("app.routes.student.update_students")
def test_update_students(
    mock_update_students,
    client,
    single_student_data,
    bulk_students_data,
    is_bulk,
    make_student_api_response,
):
    # Arrange
    if is_bulk:
        request_payload = [
            {**s, "id": i + 1, "first_name": s["first_name"] + "_Updated"}
            for i, s in enumerate(bulk_students_data)
        ]
    else:
        request_payload = {
            **single_student_data,
            "id": 1,
            "first_name": single_student_data["first_name"] + "_Updated",
        }

    items_to_process = (
        request_payload if isinstance(request_payload, list) else [request_payload]
    )
    expected_data = [
        make_student_api_response(item, id=item["id"]) for item in items_to_process
    ]
    mock_update_students.return_value = (expected_data, None)

    # Act
    response = client.put(
        "/students", data=json.dumps(request_payload), content_type="application/json"
    )

    # Assert
    assert response.status_code == 200
    mock_update_students.assert_called_once_with(request_payload)
    response_data = json.loads(response.data)

    if is_bulk:
        assert "students updated successfully" in response_data["message"]
        assert response_data["data"] == expected_data
    else:
        assert response_data["message"] == "Student updated successfully"
        assert response_data["data"] == expected_data[0]


@pytest.mark.parametrize("payload, expected_ids", [(1, [1]), ([1, 2], [1, 2])])
@patch("app.routes.student.archive_students")
def test_archive_students(mock_archive_students, client, payload, expected_ids):
    # Arrange
    mock_archive_students.return_value = expected_ids

    # Act
    response = client.patch(
        "/students", data=json.dumps(payload), content_type="application/json"
    )

    # Assert
    assert response.status_code == 200
    mock_archive_students.assert_called_once_with(payload)
    response_data = json.loads(response.data)
    assert response_data["archived_ids"] == expected_ids
    assert f"{len(expected_ids)} student(s) archived successfully" in response_data["message"]
