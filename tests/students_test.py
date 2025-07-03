import pytest
import json
from unittest.mock import patch


def test_insert_student(client):
    student_data = {
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
        "program_id": 1
    }

    with patch('routes.student.insert_student') as mock_insert_student, patch('routes.student.get_student_by_id') as mock_get_student_by_id:
        
        mock_insert_student.return_value = 1
        mock_student_row = (
            1,  # id
            student_data["first_name"],
            student_data["last_name"],
            student_data["email"],
            student_data["address"],
            student_data["city"],
            student_data["province"],
            student_data["country"],
            student_data["address_type"],
            student_data["status"],
            1 if student_data["coop"] else 0,
            0 if not student_data["is_international"] else 1,
            student_data["program_id"],
            "2025-07-01 00:00:00",  # created_at
            "2025-07-01 00:00:00",  # updated_at
            0  # is_archived
        )
        mock_get_student_by_id.return_value = mock_student_row

        response = client.post("/students", data=json.dumps(student_data), content_type="application/json")

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data["message"] == "Student inserted successfully"
        expected_data = student_data.copy()
        expected_data.update({
            "id": 1,
            "created_at": "2025-07-01 00:00:00",
            "updated_at": "2025-07-01 00:00:00",
            "is_archived": False
        })
        assert response_data["data"] == expected_data