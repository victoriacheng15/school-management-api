from typing import Callable, Any, Dict, List, Union, Tuple, Optional, Sequence
from flask import jsonify, Response


def normalize_to_list(data):
    return data if isinstance(data, list) else [data]


def handle_bulk_process(
    items: Sequence[Dict[str, Any] | Any],
    process_func: Callable[..., Any],
    success_func: Optional[Callable[..., Any]] = None,
    id_key: Optional[str] = None,
    missing_id_msg: Optional[str] = None,
    dict_to_row_func: Optional[Callable[[Dict[str, Any]], Any]] = None,
    row_to_dict_func: Optional[Callable[[Any], Dict[str, Any]]] = None,
) -> Tuple[List[Dict[str, Any] | Any] | None, Optional[Dict[str, Any]], Optional[int]]:
    """
    Generic bulk process handler for create/update/archive operations.

    Args:
    - items: list of dicts or IDs to process
    - process_func: function(item_id, row) or function(row) to perform action
    - success_func: function(item_id) to fetch full data after process
    - id_key: key in dict to get ID (for update/archive)
    - missing_id_msg: error message if ID missing in dict
    - dict_to_row_func: function to convert dict to DB row tuple (optional)
    - row_to_dict_func: function to convert DB row to dict (optional)

    Returns:
    - (list_of_success_dicts_or_ids, error_response)
    """

    items = normalize_to_list(items)
    if not items:
        return None, {"error": "Empty Payload"}, 400

    success_results: List[Dict[str, Any] | Any] = []
    errors: List[Dict[str, Any]] = []

    for idx, item in enumerate(items):
        try:
            if id_key:
                item_id = item[id_key] if isinstance(item, dict) else item
                if item_id in (None, ""):
                    errors.append(
                        {
                            "index": idx,
                            "data": item,
                            "error": missing_id_msg or "ID is required",
                        }
                    )
                    continue
            row = dict_to_row_func(item) if dict_to_row_func else item

            result = process_func(item_id, row) if id_key else process_func(row)

            if not result:
                continue
            if success_func:
                data = success_func(result if not id_key else item_id)
                if data is not None:
                    success_results.append(
                        row_to_dict_func(data) if row_to_dict_func else data
                    )
            else:
                success_results.append(item if id_key is None else item_id)
        except Exception as e:
            errors.append({"index": idx, "data": item, "error": str(e)})

    if errors:
        return None, {"errors": errors}, 400
    if not success_results:
        return None, {"error": "No records processed"}, 404

    return success_results, None, None


def api_response(
    data: Any,
    message: str = "Success",
    status_code: int = 200,
) -> Tuple[Response, int]:
    """Generic success response."""
    return jsonify({"message": message, "data": data}), status_code


def api_response_error(
    message: Union[str, dict, list],
    status_code: int = 500,
) -> Tuple[Response, int]:
    if isinstance(message, str):
        payload = {"error": message}
    else:
        payload = message
    return jsonify(payload), status_code


def build_bulk_response(
    success_list: List[Any],
    success_msg_single: str,
    success_msg_bulk: str,
    success_code: int = 200,
    created: bool = False,
) -> Tuple[Dict[str, Any], int]:
    """
    Decide between single-object vs list response
    and automatically switch to 201 when created=True.
    """
    if len(success_list) == 1:
        payload = {"message": success_msg_single, "data": success_list[0]}
    else:
        payload = {
            "message": success_msg_bulk.format(len(success_list)),
            "data": success_list,
        }

    status = 201 if created else success_code
    return payload, status


def from_bulk_result(
    data: Union[List[Any], None],
    error: Union[Dict[str, Any], None],
    status: Union[int, None],
) -> Tuple[Response, int]:
    """
    Glue code that lets you do:

        return from_bulk_result(*handle_bulk_process(...))
    """
    if error:
        return api_response_error(**error, status_code=status or 400)
    return api_response(data, status_code=status or 200)
