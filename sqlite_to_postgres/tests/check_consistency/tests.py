"""тесты для панели администратора"""

import os
from contextlib import closing
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from new_admin_panel_sprint_1.sqlite_to_postgres.db_settings import (
    DSL, POSTGRE_TABLES, SQLITE_TABLES)
from new_admin_panel_sprint_1.sqlite_to_postgres.utils import conn_context

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / '.env')


db = BASE_DIR / os.getenv('SQLITE_DB')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))

with conn_context(db) as sqlite_conn, \
        closing(psycopg2.connect(**DSL, cursor_factory=RealDictCursor)) as pg_conn:
    sqlite_cur = sqlite_conn.cursor()
    for sqlite_table_name, psql_table_name in zip(SQLITE_TABLES, POSTGRE_TABLES):
        person_count_v1 = sqlite_cur.execute(
            f"""SELECT count(*) as  count FROM {sqlite_table_name}"""
        )
        x1 = sqlite_cur.fetchone()
        with pg_conn.cursor() as pg_cur:
            person_count_v2 = pg_cur.execute(
                f"""SELECT count(*) as count FROM content.{psql_table_name}"""
            )
            x2 = pg_cur.fetchone()
        n1 = list(x1.values())[0]
        n2 = list(x2.values())[0]
        assert n1 == n2, f'{psql_table_name} - размеры не совпадают'

        person_count_v1 = sqlite_cur.execute(
            f"""SELECT * FROM {sqlite_table_name}""")
        while True:
            x1 = sqlite_cur.fetchmany(CHUNK_SIZE)
            if x1:
                idxs = tuple([str(el['id']) for el in x1])
                with pg_conn.cursor() as pg_cur:
                    pg_cur.execute(
                        f"""SELECT * FROM content.{psql_table_name} \
                            WHERE content.{psql_table_name}.id in {idxs};"""
                    )
                    x2 = pg_cur.fetchmany(CHUNK_SIZE)
                assert len(x1) == len(x2)
                for i in range(len(x1)):
                    assert x1[i] == x1[i], f'{psql_table_name} - значения не совпадают'
            else:
                break
