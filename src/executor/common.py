from datetime import timedelta


def schedule_timeout_from_request(value: int | str | None) -> timedelta | None:
    if value is None:
        return value
    elif isinstance(value, int) or value.isdigit():
        return timedelta(seconds=int(value))
    else:
        raise ValueError(value)
