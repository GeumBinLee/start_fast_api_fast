import datetime
import json
from unittest.mock import MagicMock

import pytest

from app.core.exceptions import ReturnHandler


def test_return_handler_initialization():
    handler = ReturnHandler(message="Test message", status_code=400)
    assert handler.message == "Test message"
    assert handler.status_code == 400


@pytest.fixture
def mock_request():
    mock = MagicMock()
    mock.url = "http://testserver/test"
    return mock


@pytest.fixture
def mock_dblogger():
    return MagicMock()


def test_handle_success(mock_request, mock_dblogger):
    handler = ReturnHandler(message="Success", status_code=200)
    response = handler.handle_success(request=mock_request, dblogger=mock_dblogger)

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {
        "status_code": 200,
        "message": "Success",
    }
    mock_dblogger.info.assert_called_once()


def test_handle_success_with_result(mock_request, mock_dblogger):
    handler = ReturnHandler(message="Success", status_code=200, result={"key": "value"})
    response = handler.handle_success(request=mock_request, dblogger=mock_dblogger)

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {
        "status_code": 200,
        "message": "Success",
        "result": {"key": "value"},
    }
    mock_dblogger.info.assert_called_once()


def test_handle_success_with_date(mock_request, mock_dblogger):
    result = [{"date": datetime.date(2024, 5, 24)}]
    handler = ReturnHandler(message="Success", status_code=200, result=result)
    response = handler.handle_success(request=mock_request, dblogger=mock_dblogger)

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {
        "status_code": 200,
        "message": "Success",
        "result": [{"date": "2024-05-24"}],
    }
    mock_dblogger.info.assert_called_once()


def test_handle_success_with_datetime(mock_request, mock_dblogger):
    result = [{"datetime": datetime.datetime(2024, 5, 24, 14, 30, 0)}]
    handler = ReturnHandler(message="Success", status_code=200, result=result)
    response = handler.handle_success(request=mock_request, dblogger=mock_dblogger)

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {
        "status_code": 200,
        "message": "Success",
        "result": [{"datetime": "2024-05-24 14:30:00"}],
    }
    mock_dblogger.info.assert_called_once()


def test_handle_success_with_type_error(mock_request, mock_dblogger):
    result = [{"date": datetime.date(2024, 5, 24), "value": 42}]
    handler = ReturnHandler(message="Success", status_code=200, result=result)
    response = handler.handle_success(request=mock_request, dblogger=mock_dblogger)

    assert response.status_code == 200
    assert json.loads(response.body.decode()) == {
        "status_code": 200,
        "message": "Success",
        "result": [{"date": "2024-05-24", "value": 42}],
    }
    mock_dblogger.info.assert_called_once()
