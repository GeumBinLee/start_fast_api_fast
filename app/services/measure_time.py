import timeit
from functools import wraps


def measure_execution_time(func):
    """
    함수의 실행 시간을 측정하는 데코레이터입니다.
    :param func: 측정할 함수
    :return: 실행 시간을 출력하는 래퍼 함수
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        execution_time = timeit.timeit(lambda: func(*args, **kwargs), number=1)
        print(f"라우터 '{func.__name__}'의 실행 시간: {execution_time}초")
        return func(*args, **kwargs)

    return wrapper
