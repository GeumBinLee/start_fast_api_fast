import timeit
from functools import wraps


def measure_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        execution_time = timeit.timeit(
            lambda: func(*args, **kwargs), number=1, globals=func.__globals__
        )
        print(f"라우터 '{func.__name__}'의 실행 시간: {execution_time}초")
        return func(*args, **kwargs)

    return wrapper
