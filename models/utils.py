from typing import Dict


def add_prefix_to_keys(data: Dict, prefix: str) -> Dict:
    keys = [*data.keys()]
    for key in keys:
        data[f"{prefix}_{key}"] = data.pop(key)
    return data
