import pytest

from app.services.measure_time import measure_execution_time


@measure_execution_time
def sample_function():
    return True


def test_measure_execution_time(capsys):
    result = sample_function()
    captured = capsys.readouterr()
    assert "실행 시간" in captured.out
    assert result is True
