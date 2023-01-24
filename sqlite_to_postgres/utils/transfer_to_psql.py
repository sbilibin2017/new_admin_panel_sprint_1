'''Проверка идентичности sqlite3 м postgre БД.'''

import logging
import os
import sqlite3
from dataclasses import asdict
from typing import Dict, Generator

import psycopg2
from psycopg2.extras import RealDictCursor

from new_admin_panel_sprint_1.sqlite_to_postgres.db.settings import (
    POSTGRE_TABLES, SQLITE_TABLES)
from new_admin_panel_sprint_1.sqlite_to_postgres.utils.validators import (
    Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person)


class SQLiteExtractor:
    '''Класс для извлечения данных из sqlite3 БД.'''

    def __init__(self, conn: sqlite3.Connection):
        self.sql_conn = conn.cursor()
        self.table_name = SQLITE_TABLES

    def extract_movies(self):
        '''Извлекает данные из таблицы.'''
        for table_name in self.table_name:
            self.sql_conn.execute(
                f'''SELECT * FROM {table_name}'''
            )
            while True:
                rows = self.sql_conn.fetchmany(
                    int(os.environ.get('CHUNK_SIZE')))
                if rows:
                    yield (table_name, rows)
                else:
                    break


class PostgresSaver:
    '''Класс для загрузки данных в postre БД.'''

    def __init__(self, psql_conn: RealDictCursor) -> None:
        self.psql_conn = psql_conn
        self.d_sqlite2psql_table_name = dict(
            zip(SQLITE_TABLES, POSTGRE_TABLES))

    def insert_query(
            self,
            table_name: str,
            row: Dict) -> None:
        '''Вставляет данные в таблицу.'''
        cols = ','.join(row.keys())
        qmarks = ','.join(['%s' for s in row.keys()])
        values = tuple(row.values())
        insert_statement = f'INSERT INTO content.{table_name} \
            ({cols}) VALUES ({qmarks}) ON CONFLICT DO NOTHING;'
        with self.psql_conn.cursor() as cur:
            try:
                cur.execute(insert_statement, values)
                self.psql_conn.commit()
            except psycopg2.Error as error:
                logging.exception(error)

    def validate_person(self, row):
        '''Валидация персоны.'''
        created = Person(
            id=row['id'],
            full_name=row['full_name'],
            created_at=row['created_at'] or Person.created_at,
            updated_at=row['updated_at'] or Person.updated_at
        )

        return created

    def validate_genre(self, row):
        '''Валидация жанра.'''
        created = Genre(
            id=row['id'],
            name=row['name'] or Genre.name,
            description=row['description'] or Genre.description,
            created_at=row['created_at'] or Genre.created_at,
            updated_at=row['updated_at'] or Genre.updated_at
        )

        return created

    def validate_filmwork(self, row):
        '''Валидация кинопроизведения.'''
        created = Filmwork(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            creation_date=row['creation_date'],
            file_path=row['file_path'] or Filmwork.file_path,
            rating=row['rating'] or Filmwork.rating,
            type=row['type'] or Filmwork.type,
            created_at=row['created_at'] or Filmwork.created_at,
            updated_at=row['updated_at'] or Filmwork.updated_at
        )

        return created

    def validate_filmwork_genre(self, row):
        '''Валидация жанра кинопроизведения.'''
        created = FilmworkGenre(
            id=row['id'],
            filmwork_id=row['film_work_id'],
            genre_id=row['genre_id'],
            created_at=row['created_at'] or FilmworkGenre.created_at
        )

        return created

    def validate_filmwork_person(self, row):
        '''Валидация персоны кинопроизведения.'''
        created = FilmworkPerson(
            id=row['id'],
            filmwork_id=row['film_work_id'],
            person_id=row['person_id'],
            role=row['role'] or FilmworkPerson.role,
            created_at=row['created_at'] or FilmworkPerson.created_at
        )

        return created

    def save_all_data(self, gen: Generator) -> None:
        '''Валидирует данные и вставляет их в БД.'''
        for tup in gen:
            table_name, rows = tup
            table_name = self.d_sqlite2psql_table_name[table_name]
            print(table_name)
            for row in rows:
                if table_name == 'person':
                    created = self.validate_person(row)
                elif table_name == 'genre':
                    created = self.validate_genre(row)
                elif table_name == 'filmwork':
                    created = self.validate_filmwork(row)
                elif table_name == 'filmwork_person':
                    created = self.validate_filmwork_person(row)
                elif table_name == 'filmwork_genre':
                    created = self.validate_filmwork_genre(row)
                row_validated = asdict(created)
                self.insert_query(
                    table_name=table_name,
                    row=row_validated
                )
