from unittest.mock import MagicMock, patch

import pytest
from pymysql import OperationalError

from app.config.database import execute_query, get_db_connection, transaction_queries
from app.core.exceptions import ReturnHandler


@patch("app.config.database.pymysql.connect")
def test_get_db_connection(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    conn = get_db_connection()
    mock_connect.assert_called_once()
    assert conn == mock_conn
    conn.close()


@patch("app.config.database.pymysql.connect")
def test_execute_query(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    mock_cursor.fetchone.return_value = (1,)

    query = "SELECT 1"
    result = execute_query(query, method="fetchone")
    assert result == (1,)
    mock_conn.commit.assert_called_once()
    mock_conn.close()


@patch("app.config.database.pymysql.connect")
def test_execute_query_exception(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    mock_cursor.execute.side_effect = OperationalError

    query = "SELECT 1"
    with pytest.raises(ReturnHandler):
        execute_query(query, method="fetchone")
    mock_conn.rollback.assert_called_once()
    mock_conn.close()


@patch("app.config.database.pymysql.connect")
def test_transaction_queries(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Define the behavior of fetchone for each query
    mock_cursor.fetchone.side_effect = [(1,), (2,)]

    queries = ["SELECT 1", "SELECT 2"]
    results = transaction_queries(queries, method="fetchone")

    assert results == [(1,), (2,)]
    mock_conn.commit.assert_called_once()
    mock_conn.close()


@patch("app.config.database.pymysql.connect")
def test_transaction_queries_exception(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    mock_cursor.execute.side_effect = OperationalError

    queries = ["SELECT 1"]
    with pytest.raises(ReturnHandler):
        transaction_queries(queries, method="fetchone")
    mock_conn.rollback.assert_called_once()
    mock_conn.close()


@patch("app.config.database.pymysql.connect")
def test_transaction_queries_with_select(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Define the behavior of fetchone for each query
    mock_cursor.fetchone.side_effect = [(1,), (2,)]

    queries = ["SELECT 1", "INSERT INTO table (column) VALUES ({select})"]
    results = transaction_queries(queries, method="fetchone", select=0)

    assert results == [(1,), (2,)]
    mock_conn.commit.assert_called_once()
    mock_conn.close()
