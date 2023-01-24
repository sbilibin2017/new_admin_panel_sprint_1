'''Главный модуль.'''

import logging
import os
from contextlib import closing
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from new_admin_panel_sprint_1.sqlite_to_postgres.db.settings import DSL
from new_admin_panel_sprint_1.sqlite_to_postgres.utils.load_from_sqlite import \
    load_from_sqlite
from new_admin_panel_sprint_1.sqlite_to_postgres.utils.sqlite_context_manager import \
    conn_context

# корень проекта
BASE_DIR = Path(__file__).resolve().parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / '.env')
# инициализируем логгер
logging.basicConfig(
    filename=BASE_DIR / 'load_data.log',
    encoding='utf-8',
    format='%(asctime)s %(message)s',
    level=logging.DEBUG
)
# путь до sqlite БД
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'db', os.environ.get('SQLITE_DB'))


if __name__ == '__main__':
    with conn_context(SQLITE_DB_PATH) as sqlite_conn, \
            closing(psycopg2.connect(**DSL, cursor_factory=RealDictCursor)) as pg_conn:
        sqlite_cur = sqlite_conn.cursor()
        load_from_sqlite(sqlite_conn, pg_conn)
