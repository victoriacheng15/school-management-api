from .routes_helpers import normalize_to_list

def bulk_create_entities(
    data,
    *,
    insert_func,        # function to insert a single row, returns new ID
    to_row_func,        # converts dict to DB row format
    to_dict_func,       # converts DB row to dict for response
    read_by_ids_func,   # reads rows by list of IDs
    no_success_msg="No entities were created.",
    success_status_code=201,
    failure_status_code=400,
):
    items = normalize_to_list(data)
    created_ids = []
    errors = []

    for item in items:
        # Clean string fields
        if isinstance(item, dict):
            item = {k: (v.strip() if isinstance(v, str) else v) for k, v in item.items()}

        try:
            row = to_row_func(item)
            new_id = insert_func(row)
            if new_id:
                created_ids.append(new_id)
            else:
                errors.append({"message": "Failed to insert entity (unknown DB error)."})
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": no_success_msg, "details": errors}, failure_status_code

    created_rows = read_by_ids_func(created_ids)
    created_entities = [to_dict_func(row) for row in created_rows]

    return created_entities, None, success_status_code


def bulk_update_entities(
    data,
    *,
    update_func,        # function to update entity by ID and row, returns True/False
    get_existing_func,  # function to read existing entity by ID
    to_row_func,        # converts dict to DB row format
    to_dict_func,       # converts DB row to dict for response
    read_by_ids_func,   # reads rows by list of IDs
    no_success_msg="No entities were updated.",
    missing_id_msg="Missing entity ID for update.",
    not_found_msg="Entity ID {id} not found.",
    not_updated_msg="Entity ID {id} not updated.",
    success_status_code=200,
    failure_status_code=400,
):
    items = normalize_to_list(data)
    updated_ids = []
    errors = []

    for item in items:
        # Clean string fields
        if isinstance(item, dict):
            item = {k: (v.strip() if isinstance(v, str) else v) for k, v in item.items()}

        entity_id = item.get("id")
        if not entity_id:
            errors.append({"message": missing_id_msg})
            continue

        existing = get_existing_func(entity_id)
        if not existing:
            errors.append({"message": not_found_msg.format(id=entity_id)})
            continue

        # Merge incoming data over existing data
        if not isinstance(existing, dict):
            existing = to_dict_func(existing)
        merged = {**existing, **item}

        try:
            row = to_row_func(merged)
            success = update_func(entity_id, row)
            if success:
                updated_ids.append(entity_id)
            else:
                errors.append({"message": not_updated_msg.format(id=entity_id)})
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, failure_status_code

    updated_rows = read_by_ids_func(updated_ids)
    updated_entities = [to_dict_func(row) for row in updated_rows]

    return updated_entities, errors if errors else None, success_status_code


def bulk_archive_entities(
    ids,
    *,
    archive_func,       # function to archive entity by ID, returns rows updated count
    get_existing_func,  # function to read existing entity by ID
    to_dict_func,       # converts DB row to dict for response
    read_by_ids_func,   # reads rows by list of IDs
    no_success_msg="No entities were archived.",
    id_type=int,
    missing_id_msg="Invalid ID.",
    not_found_msg="Entity ID {id} not found or already archived.",
    not_updated_msg="Entity ID {id} not archived.",
    success_status_code=200,
    failure_status_code=422,
):
    normalized_ids = normalize_to_list(ids)
    if not all(isinstance(i, id_type) for i in normalized_ids):
        return [], [{"message": f"All IDs must be of type {id_type.__name__}"}], 400

    archived_ids = []
    errors = []

    for entity_id in normalized_ids:
        existing = get_existing_func(entity_id)
        if not existing:
            errors.append({"message": not_found_msg.format(id=entity_id)})
            continue

        try:
            rows_updated = archive_func(entity_id)
            if rows_updated > 0:
                archived_ids.append(entity_id)
            else:
                errors.append({"message": not_updated_msg.format(id=entity_id)})
        except Exception as e:
            errors.append({"message": str(e)})

    if not archived_ids:
        return [], errors, failure_status_code

    archived_rows = read_by_ids_func(archived_ids)
    archived_entities = [to_dict_func(row) for row in archived_rows]

    return archived_entities, errors if errors else None, success_status_code
