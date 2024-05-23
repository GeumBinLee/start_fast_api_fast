import time
from typing import Dict, List, Tuple, Union

import pymysql

from app.config.settings import get_settings
from app.core.exceptions import ReturnHandler

settings = get_settings()


def get_db_connection():
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_database,
        port=settings.db_port,
    )


def execute_query(query: str, params: Tuple = None, method: str = "fetchall"):
    start_time = time.time()
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            result = None
            if method == "fetchall":
                result = cur.fetchall()
            elif method == "fetchone":
                result = cur.fetchone()
            elif method == "fetchmany":
                result = cur.fetchmany()
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
    start_time = time.time()
    results = []
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for query, param in zip(queries, params or [()] * len(queries)):
                if (
                    results
                    and not query.strip().lower().startswith("select")
                    and select is not None
                ):
                    query = query.format(select=results[select])

                try:
                    cur.execute(query, param)
                except:
                    cur.execute(query.format(*param))

                rows = None
                if method == "fetchall":
                    rows = cur.fetchall()
                elif method == "fetchone":
                    rows = cur.fetchone()
                elif method == "fetchmany":
                    rows = cur.fetchmany()

                if rows:
                    results.append(rows[0] if cur.rowcount == 1 else rows)
            conn.commit()
            return results
    except pymysql.err.Error as e:
        conn.rollback()
        raise ReturnHandler(e, start_time, query, param)
    finally:
        conn.close()
