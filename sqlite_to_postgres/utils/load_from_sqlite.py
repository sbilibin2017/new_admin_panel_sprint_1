import sqlite3

from psycopg2.extensions import connection as _connection

from new_admin_panel_sprint_1.sqlite_to_postgres.utils.transfer_to_psql import (
    PostgresSaver, SQLiteExtractor)


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection) -> None:
    '''Основной метод загрузки данных из SQLite в Postgres'''
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)
    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)
