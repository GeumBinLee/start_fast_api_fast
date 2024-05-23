import time
from typing import Dict, List, Tuple, Union

import pymysql

from app.config.settings import get_settings
from app.core.exceptions import ReturnHandler

settings = get_settings()

def get_db_connection():
    """
    데이터베이스 연결을 설정하고 반환합니다.
    :return: pymysql.connections.Connection 객체
    """
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_database,
        port=settings.db_port,
    )

def execute_query(query: str, params: Tuple = None, method: str = "fetchall"):
    """
    주어진 쿼리를 실행하고 결과를 반환합니다.
    :param query: SQL 쿼리 문자열
    :param params: 쿼리 파라미터 튜플
    :param method: 결과를 반환하는 방법 ('fetchall', 'fetchone', 'fetchmany')
    :return: 쿼리 결과
    """
    start_time = time.time()
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            result = getattr(cur, method)() if method != "execute" else None
            conn.commit()
            return result
    except pymysql.err.Error as e:
        conn.rollback()
        raise ReturnHandler(e, start_time, query, params)
    finally:
        conn.close()

def transaction_queries(
    queries: List[str],
    params: Union[List[Tuple], List[Dict]] = None,
    method: str = "execute",
    select: int = None,
) -> List:
    """
    트랜잭션으로 여러 쿼리를 실행하고 결과를 반환합니다.
    :param queries: SQL 쿼리 문자열 목록
    :param params: 각 쿼리에 대한 파라미터 목록
    :param method: 결과를 반환하는 방법 ('fetchall', 'fetchone', 'fetchmany', 'execute')
    :param select: 이전 쿼리 결과를 참조하는 인덱스
    :return: 쿼리 결과 목록
    """
    start_time = time.time()
    results = []
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for query, param in zip(queries, params or [()] * len(queries)):
                if results and not query.strip().lower().startswith("select") and select is not None:
                    query = query.format(select=results[select])
                cur.execute(query, param or ())
                rows = getattr(cur, method)() if method != "execute" else None
                if rows:
                    results.append(rows[0] if cur.rowcount == 1 else rows)
            conn.commit()
            return results
    except pymysql.err.Error as e:
        conn.rollback()
        raise ReturnHandler(e, start_time, query, param)
    finally:
        conn.close()
