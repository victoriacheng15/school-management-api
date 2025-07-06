import pytest
import json
from unittest.mock import patch


@pytest.mark.parametrize("is_bulk", [False, True])
def test_create_student(
    client, is_bulk, single_student_data, bulk_students_data, make_student_row
):
    payload = bulk_students_data if is_bulk else single_student_data

    with (
        patch("app.routes.student.create_student") as mock_create_student,
        patch("app.routes.student.read_student_by_id") as mock_read_student_by_id,
    ):
        if is_bulk:
            mock_create_student.side_effect = [1, 2]
            mock_read_student_by_id.side_effect = [
                make_student_row(bulk_students_data[0], id=1),
                make_student_row(bulk_students_data[1], id=2),
            ]
        else:
            mock_create_student.return_value = 1
            mock_read_student_by_id.return_value = make_student_row(
                single_student_data, id=1
            )

        response = client.post(
            "/students", data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 201
        response_data = json.loads(response.data)

        if is_bulk:
            assert "students created successfully" in response_data["message"]
            assert isinstance(response_data["data"], list)
            assert len(response_data["data"]) == len(payload)
            for idx, student in enumerate(response_data["data"]):
                expected = payload[idx].copy()
                expected.update(
                    {
                        "id": idx + 1,
                        "created_at": "2025-07-01 00:00:00",
                        "updated_at": "2025-07-01 00:00:00",
                        "is_archived": False,
                    }
                )
                assert student == expected
        else:
            assert response_data["message"] == "Student created successfully"
            expected = payload.copy()
            expected.update(
                {
                    "id": 1,
                    "created_at": "2025-07-01 00:00:00",
                    "updated_at": "2025-07-01 00:00:00",
                    "is_archived": False,
                }
            )
            assert response_data["data"] == expected


def test_read_student_by_id(client, single_student_data, make_student_row):
    mock_student_row = make_student_row(single_student_data, id=1)
    expected_data = single_student_data.copy()
    expected_data.update(
        {
            "id": 1,
            "coop": 1,
            "is_international": 0,
            "created_at": "2025-07-01 00:00:00",
            "updated_at": "2025-07-01 00:00:00",
            "is_archived": 0,
        }
    )

    with patch("app.routes.student.read_student_by_id") as mock_read_student_by_id:
        mock_read_student_by_id.return_value = mock_student_row

        response = client.get("/students/1")
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data == expected_data


def test_read_student_by_id_not_found(client):
    with patch("app.routes.student.read_student_by_id") as mock_read_student_by_id:
        mock_read_student_by_id.return_value = None

        response = client.get("/students/999")
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data["error"] == "Student not found"


@pytest.mark.parametrize("is_bulk", [False, True])
def test_update_students(client, single_student_data, bulk_students_data, make_student_row, is_bulk):
    data = bulk_students_data if is_bulk else single_student_data
    payload = []

    if is_bulk:
        for idx, d in enumerate(data, start=1):
            updated = d.copy()
            updated["id"] = idx
            updated["first_name"] += "_Updated"
            payload.append(updated)
    else:
        updated = data.copy()
        updated["id"] = 1
        updated["first_name"] += "_Updated"
        payload = updated

    with patch("app.routes.student.update_student") as mock_update_student, \
         patch("app.routes.student.read_student_by_id") as mock_read_student_by_id:

        if is_bulk:
            mock_update_student.side_effect = [1, 1]
            mock_read_student_by_id.side_effect = [
                make_student_row(student, id=idx+1)
                for idx, student in enumerate(bulk_students_data)
            ]
        else:
            mock_update_student.return_value = 1
            mock_read_student_by_id.return_value = make_student_row(single_student_data, id=1)

        response = client.put("/students", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 200
        response_data = json.loads(response.data)

        if is_bulk:
            assert "students updated successfully" in response_data["message"]
            assert isinstance(response_data["data"], list)
            assert len(response_data["data"]) == len(payload)
        else:
            assert response_data["message"] == "Student updated successfully"
            assert isinstance(response_data["data"], dict)
            assert response_data["data"]["id"] == 1


@pytest.mark.parametrize("ids", [[1], [1, 2]])
def test_archive_students(client, ids):
    with patch("app.routes.student.archive_student") as mock_archive_student:
        mock_archive_student.side_effect = [1 for _ in ids]

        response = client.patch(
            "/students",
            data=json.dumps(ids if len(ids) > 1 else ids[0]),
            content_type="application/json",
        )

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data["archived_ids"] == ids
        assert "archived successfully" in response_data["message"]
