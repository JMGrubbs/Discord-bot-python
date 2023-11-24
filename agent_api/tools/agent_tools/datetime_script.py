import datetime

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime('%Y-%m-%d %H:%M:%S')

def test_get_current_datetime():
    assert get_current_datetime() == datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')