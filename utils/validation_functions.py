from dateutil.parser import parse
from dateutil.parser import ParserError


def validate_field(data, field_name, datatype):
    value = data.get(field_name)
    if value is None:
        return None

    try:
        if datatype == "datetime":
            parse(value)
        elif datatype == "int":
            int(value)
        elif datatype == "float":
            float(value)
        else:
            return f"Unsupported datatype '{datatype}' for field '{field_name}'."
    except (ParserError, TypeError, ValueError):
        return f"'{field_name}' must be a valid {datatype}."

    return None
