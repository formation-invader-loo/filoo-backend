"""Some functions to parse/decode/encode JSON
"""
import json

def pretty_json(object: any, indentation: int = 4) -> str:
    """Encode a Python object in JSON

    Args:
        object (any): Python object to encode
        indentation (int): indentations per level used to pretty print

    Returns:
        str: JSON string of given object
    """
    json_str = json.JSONEncoder().encode(object)
    json_str = json.loads(json_str)
    json_str = json.dumps(json_str, indent=indentation)
    return json_str