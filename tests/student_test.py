import pytest
import json
from unittest.mock import patch

@pytest.mark.parametrize("is_bulk", [False, True])
def test_insert_student(client, is_bulk, single_student_data, bulk_students_data, make_student_row):
    payload = bulk_students_data if is_bulk else single_student_data

    with patch("app.routes.student.insert_student") as mock_insert_student, \
         patch("app.routes.student.get_student_by_id") as mock_get_student_by_id:

        if is_bulk:
            mock_insert_student.side_effect = [1, 2]
            mock_get_student_by_id.side_effect = [
                make_student_row(bulk_students_data[0], id=1),
                make_student_row(bulk_students_data[1], id=2),
            ]
        else:
            mock_insert_student.return_value = 1
            mock_get_student_by_id.return_value = make_student_row(single_student_data, id=1)

        response = client.post("/students", data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 201
        response_data = json.loads(response.data)

        if is_bulk:
            assert "students inserted successfully" in response_data["message"]
            assert isinstance(response_data["data"], list)
            assert len(response_data["data"]) == len(payload)
            for idx, student in enumerate(response_data["data"]):
                expected = payload[idx].copy()
                expected.update({
                    "id": idx + 1,
                    "created_at": "2025-07-01 00:00:00",
                    "updated_at": "2025-07-01 00:00:00",
                    "is_archived": False,
                })
                assert student == expected
        else:
            assert response_data["message"] == "Student inserted successfully"
            expected = payload.copy()
            expected.update({
                "id": 1,
                "created_at": "2025-07-01 00:00:00",
                "updated_at": "2025-07-01 00:00:00",
                "is_archived": False,
            })
            assert response_data["data"] == expected

def test_get_student_by_id(client, single_student_data, make_student_row):
    mock_student_row = make_student_row(single_student_data, id=1)
    expected_data = single_student_data.copy()
    expected_data.update({
        "id": 1,
        "coop": 1,
        "is_international": 0,
        "created_at": "2025-07-01 00:00:00",
        "updated_at": "2025-07-01 00:00:00",
        "is_archived": 0,
    })

    with patch("app.routes.student.get_student_by_id") as mock_get_student_by_id:
        mock_get_student_by_id.return_value = mock_student_row

        response = client.get("/students/1")
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data == expected_data

def test_get_student_by_id_not_found(client):
    with patch("app.routes.student.get_student_by_id") as mock_get_student_by_id:
        mock_get_student_by_id.return_value = None

        response = client.get("/students/999")
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data["error"] == "Student not found"