import time


def is_enable(start_time: int, end_time: int):
    current_time = int(time.time())
    if start_time < current_time and end_time > current_time:
        return True
    return False
