import os
from pathlib import Path

from dotenv import load_dotenv

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / '.env')
# подключение к постгрес БД
DSL = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
}
# таблицы
TABLES = ('person', 'genre', 'filmwork',
          'filmwork_genre', 'filmwork_person')
