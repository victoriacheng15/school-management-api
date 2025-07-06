import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


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
def make_student_row():
    def _make(
        data: dict,
        id=1,
        created_at="2025-07-01 00:00:00",
        updated_at="2025-07-01 00:00:00",
        is_archived=0,
    ):
        return (
            id,
            data["first_name"],
            data["last_name"],
            data["email"],
            data["address"],
            data["city"],
            data["province"],
            data["country"],
            data["address_type"],
            data["status"],
            int(data["coop"]),
            int(data["is_international"]),
            data["program_id"],
            created_at,
            updated_at,
            is_archived,
        )

    return _make
