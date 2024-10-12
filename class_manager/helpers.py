def flatten_dict(original_dict, parent_key=""):
    items = []
    for key, value in original_dict.items():
        new_key = f"{parent_key}/{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)