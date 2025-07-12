import pytest

routes_to_test = [
    "/",
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
def test_routes_return_200_and_data(client, route):
    response = client.get(route)
    assert response.status_code == 200
    assert response.is_json

    json_data = response.get_json()

    if route == "/":
        assert "message" in json_data
        assert "status" in json_data
        assert "version" in json_data
        assert "available_routes" in json_data
        assert isinstance(json_data["available_routes"], list)
    elif route == "/students":
        assert "message" in json_data
        assert "data" in json_data
        assert isinstance(json_data["data"], list)
        assert len(json_data["data"]) > 0
    else:
        # For other collection routes, they directly return a list of dictionaries
        assert isinstance(json_data, list)
        assert len(json_data) > 0
