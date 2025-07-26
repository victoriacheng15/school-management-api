import pytest
from unittest.mock import MagicMock
from app.utils.routes_helpers import normalize_to_list, handle_bulk_process


# Tests for normalize_to_list
def test_normalize_to_list_single_item():
    assert normalize_to_list(1) == [1]
    assert normalize_to_list("test") == ["test"]
    assert normalize_to_list({"key": "value"}) == [{"key": "value"}]


def test_normalize_to_list_list_item():
    assert normalize_to_list([1, 2, 3]) == [1, 2, 3]
    assert normalize_to_list([]) == []


# Tests for handle_bulk_process
@pytest.fixture
def mock_funcs():
    return {
        "process_func": MagicMock(return_value=1),
        "success_func": MagicMock(return_value={"id": 1, "name": "Test"}),
        "dict_to_row_func": MagicMock(side_effect=lambda x: (x["name"],)),
        "row_to_dict_func": MagicMock(side_effect=lambda x: {"id": x, "name": "Test"}),
    }


def test_handle_bulk_process_create_success(mock_funcs):
    items = [{"name": "Item1"}, {"name": "Item2"}]
    results, error_data, error_code = handle_bulk_process(
        items=items,
        process_func=mock_funcs["process_func"],
        success_func=mock_funcs["success_func"],
        dict_to_row_func=mock_funcs["dict_to_row_func"],
        row_to_dict_func=mock_funcs["row_to_dict_func"],
    )

    assert error_data is None
    assert error_code is None
    assert len(results) == 2
    assert mock_funcs["process_func"].call_count == 2
    assert mock_funcs["success_func"].call_count == 2
    assert mock_funcs["dict_to_row_func"].call_count == 2
    assert mock_funcs["row_to_dict_func"].call_count == 2


def test_handle_bulk_process_update_success(mock_funcs):
    items = [{"id": 1, "name": "UpdatedItem1"}]
    mock_funcs["process_func"].return_value = 1
    results, error_data, error_code = handle_bulk_process(
        items=items,
        process_func=mock_funcs["process_func"],
        success_func=mock_funcs["success_func"],
        id_key="id",
        missing_id_msg="Missing ID",
        dict_to_row_func=mock_funcs["dict_to_row_func"],
        row_to_dict_func=mock_funcs["row_to_dict_func"],
    )

    assert error_data is None
    assert error_code is None
    assert len(results) == 1
    assert mock_funcs["process_func"].call_count == 1
    assert mock_funcs["success_func"].call_count == 1
    assert mock_funcs["dict_to_row_func"].call_count == 1
    assert mock_funcs["row_to_dict_func"].call_count == 1


def test_handle_bulk_process_no_records_processed(mock_funcs):
    items = [{"name": "Item1"}]
    mock_funcs["process_func"].return_value = 0
    results, error_data, error_code = handle_bulk_process(
        items=items,
        process_func=mock_funcs["process_func"],
        success_func=mock_funcs["success_func"],
        dict_to_row_func=mock_funcs["dict_to_row_func"],
        row_to_dict_func=mock_funcs["row_to_dict_func"],
    )

    assert results is None
    assert error_data == {"error": "No records processed"}
    assert error_code == 404


def test_handle_bulk_process_missing_id_for_update(mock_funcs):
    items = [{"name": "Item1"}]  # Missing 'id'
    results, error_data, error_code = handle_bulk_process(
        items=items,
        process_func=mock_funcs["process_func"],
        success_func=mock_funcs["success_func"],
        id_key="id",
        missing_id_msg="Missing ID",
        dict_to_row_func=mock_funcs["dict_to_row_func"],
        row_to_dict_func=mock_funcs["row_to_dict_func"],
    )

    assert results is None
    assert error_data == {"errors": [{"index": 0, "data": {"name": "Item1"}, "error": "'id'"}]}
    assert error_code == 400
