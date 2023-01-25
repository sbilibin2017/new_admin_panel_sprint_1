'''Проверка идентичности sqlite3 м postgre БД.'''

import os
import sqlite3
from dataclasses import asdict
from typing import Dict, Generator

import psycopg2
from psycopg2.extras import RealDictCursor

from new_admin_panel_sprint_1.sqlite_to_postgres.db.settings import (
    POSTGRE_TABLES, SQLITE_TABLES)
from new_admin_panel_sprint_1.sqlite_to_postgres.utils.logger import logger
from new_admin_panel_sprint_1.sqlite_to_postgres.utils.validators import (
    Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person)


class SQLiteExtractor:
    '''Класс для извлечения данных из sqlite3 БД.'''

    def __init__(self, conn: sqlite3.Connection):
        # подключение к sqlite
        self.sql_conn = conn.cursor()
        # названия таблиц
        self.table_name = SQLITE_TABLES

    def extract_movies(self):
        '''Извлекает данные из таблицы.'''
        # для каждой таблицы
        for table_name in self.table_name:
            # выбираем данные
            self.sql_conn.execute(
                f'''SELECT * FROM {table_name}'''
            )
            # пока в результате запроса есть данные
            while True:
                # отдаем данные чанками по 1000 записей
                rows = self.sql_conn.fetchmany(
                    int(os.environ.get('CHUNK_SIZE')))
                if rows:
                    yield (table_name, rows)
                else:
                    break


class PostgresSaver:
    '''Класс для загрузки данных в postre БД.'''

    def __init__(self, psql_conn: RealDictCursor) -> None:
        # подключение к postgre
        self.psql_conn = psql_conn
        # маппинг названий между sqlite и postgre
        self.d_sqlite2psql_table_name = dict(
            zip(SQLITE_TABLES, POSTGRE_TABLES))
        # датаклассы для валидации
        self.dataclasses = dict(
            zip(POSTGRE_TABLES, (Person, Genre, Filmwork, FilmworkGenre, FilmworkPerson)))
        # счетчик записей в таблицах
        self.row_counters = dict(
            zip(POSTGRE_TABLES, [0] * len(POSTGRE_TABLES)))

    def insert_query(
            self,
            table_name: str,
            row: Dict) -> None:
        '''Вставляет данные в таблицу.'''
        # список ключей
        cols = ','.join(row.keys())
        # метки для запроса
        qmarks = ','.join(['%s' for s in row.keys()])
        # значения
        values = tuple(row.values())
        # запрос для вставки данных в БД
        insert_statement = f'INSERT INTO content.{table_name} \
            ({cols}) VALUES ({qmarks}) ON CONFLICT DO NOTHING;'
        with self.psql_conn.cursor() as cur:
            try:
                cur.execute(insert_statement, values)
                self.psql_conn.commit()
            except psycopg2.Error as error:
                logger.exception(error)

    def validate(self, model, data):
        '''Валидирует данные.'''
        return asdict(model(**data))

    def fix_filmwork_id(self, table_name: str, row: dict) -> dict:
        '''Заменяет ключ film_work_id на filmwork_id.'''
        if table_name in ('filmwork_genre', 'filmwork_person'):
            row['filmwork_id'] = row['film_work_id']
            del row['film_work_id']
        return row

    def save_all_data(self, gen: Generator) -> None:
        '''Валидирует данные и вставляет их в БД.'''
        for tup in gen:
            # таблица, данные
            table_name, rows = tup
            table_name = self.d_sqlite2psql_table_name[table_name]
            logger.info(f'Таблица: {table_name}')
            # для каждой строки в данных
            for row in rows:
                # переименовывем ключи
                row = self.fix_filmwork_id(table_name, row)
                # валидируем данные
                row_validated = self.validate(
                    self.dataclasses[table_name], row)
                # вставляем данные в постргрес БД
                self.insert_query(
                    table_name=table_name,
                    row=row_validated
                )
                # увеличиваем счетчик строк
                self.row_counters[table_name] += 1
            logger.info(f'Число строк в таблицах: {self.row_counters}')
