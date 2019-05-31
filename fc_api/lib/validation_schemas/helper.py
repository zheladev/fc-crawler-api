from datetime import datetime


def validate_date_string(field, value, error):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except (ValueError, TypeError) as e:
        error(field, str(e))


def validate_int_string(field, value, error):
    try:
        int(value)
    except ValueError as e:
        error(field, str(e))
