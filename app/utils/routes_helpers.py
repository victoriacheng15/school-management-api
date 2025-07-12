from flask import jsonify

def normalize_to_list(data):
    return data if isinstance(data, list) else [data]


def handle_bulk_process(
    items,
    process_func,
    success_func=None,
    id_key=None,
    missing_id_msg=None,
    dict_to_row_func=None,
    row_to_dict_func=None,
):
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
    success_results = []

    for item in items:
        if id_key:
            item_id = item.get(id_key)
            if not item_id:
                return None, {"error": missing_id_msg}, 400

            row = dict_to_row_func(item) if dict_to_row_func else item
            result = process_func(item_id, row)
        else:
            row = dict_to_row_func(item) if dict_to_row_func else item
            result = process_func(row)

        if success_func and result:
            data = success_func(result if not id_key else item_id)
            if data:
                if row_to_dict_func:
                    success_results.append(row_to_dict_func(data))
                else:
                    success_results.append(data)
        elif result:
            success_results.append(item if id_key is None else item_id)

    if not success_results:
        return None, {"error": "No records processed"}, 404

    return success_results, None, None


def build_bulk_response(
    success_list, success_msg_single, success_msg_bulk, success_code=200, created=False
):
    if len(success_list) == 1:
        msg = success_msg_single
        data = success_list[0]
    else:
        msg = success_msg_bulk.format(len(success_list))
        data = success_list
 
    return {"message": msg, "data": data}, 201 if created else success_code

def api_response(data, message="Success", status_code=200):
    return jsonify({"message": message, "data": data}), status_code

def api_response_error(message="An error occurred", status_code=500):
    return jsonify({"error": message}), status_code
