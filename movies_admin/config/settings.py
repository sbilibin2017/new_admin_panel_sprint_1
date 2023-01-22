'''Модуль с настройками django проекта.'''

# импорт библиотек
import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / '.env')
# секрет джанго
SECRET_KEY = os.getenv('SECRET_KEY')
# режим запуска
DEBUG = os.getenv('DEBUG') == 'True'
# доступные порты в режиме деплоя (DEBUG=False)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
# для панели дебага
INTERNAL_IPS = os.getenv('INTERNAL_IPS').split(',')
# контроллеры
ROOT_URLCONF = 'config.urls'
# вебсервер
WSGI_APPLICATION = 'config.wsgi.application'
# компоненты, выведенные в отдельный модуль
include(
    'components/databases.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/auth_password_validators.py',
)
# язык
LANGUAGE_CODE = 'ru-RU'
# время
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# директория со стотическими файлами
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# директория с локализацией
LOCALE_PATHS = ['movies/locale']
