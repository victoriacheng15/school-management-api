import pytest

routes_to_test = [
    "/students",
    "/instructors",
    "/departments",
    "/programs",
    "/courses",
    "/terms",
    "/enrollments",
    "/assignments",
    "/course_schedule",
]


@pytest.mark.parametrize("route", routes_to_test)
def test_routes_return_200(client, route):
    response = client.get(route)
    assert response.status_code == 200
