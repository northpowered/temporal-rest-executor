from executor.common import schedule_timeout_from_request
from datetime import timedelta


def test_schedule_timeout_builder():

    assert schedule_timeout_from_request(None) is None
    assert schedule_timeout_from_request(3) == timedelta(seconds=3)
    assert schedule_timeout_from_request("3") == timedelta(seconds=3)
    try:
        schedule_timeout_from_request("foo")
    except Exception as ex:
        assert isinstance(ex, ValueError)
