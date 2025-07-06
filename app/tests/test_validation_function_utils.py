from ..utils.validation_functions import validate_field


def test_validate_field_datetime_valid():
    data = {"scheduled_at": "2025-07-06T14:30:00"}
    assert validate_field(data, "scheduled_at", "datetime") is None


def test_validate_field_datetime_invalid():
    data = {"scheduled_at": "not-a-date"}
    err = validate_field(data, "scheduled_at", "datetime")
    assert err == "'scheduled_at' must be a valid datetime."


def test_validate_field_int_valid():
    data = {"target_sets": "5"}
    assert validate_field(data, "target_sets", "int") is None


def test_validate_field_int_invalid():
    data = {"target_sets": "five"}
    err = validate_field(data, "target_sets", "int")
    assert err == "'target_sets' must be a valid int."


def test_validate_field_float_valid():
    data = {"target_weight": "10.5"}
    assert validate_field(data, "target_weight", "float") is None


def test_validate_field_float_invalid():
    data = {"target_weight": "heavy"}
    err = validate_field(data, "target_weight", "float")
    assert err == "'target_weight' must be a valid float."


def test_validate_field_missing_key():
    data = {}
    # Should return None if field is not present
    assert validate_field(data, "missing_field", "int") is None


def test_validate_field_unsupported_datatype():
    data = {"field": "value"}
    err = validate_field(data, "field", "unsupported")
    assert err == "Unsupported datatype 'unsupported' for field 'field'."
