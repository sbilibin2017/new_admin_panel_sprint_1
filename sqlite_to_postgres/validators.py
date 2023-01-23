import uuid
from dataclasses import dataclass, field
from datetime import datetime

DEFAULT_VALUE = ''


@dataclass
class TimeStampedMixin():
    """Класс для представления дат."""
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    class Meta:
        abstract = True


@dataclass
class UUIDMixin():
    """Класс для хэш-идентификатора"""
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    class Meta:
        abstract = True


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    """Класс для представления персоны."""
    full_name: str = field(default=DEFAULT_VALUE)


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    """Класс для представления жанра."""
    name: str = field(default=DEFAULT_VALUE)
    description: str = field(default=DEFAULT_VALUE)


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    """Класс для представления кинопроизведения."""
    title: str = field(default=DEFAULT_VALUE)
    description: str = field(default=DEFAULT_VALUE)
    creation_date: datetime = field(default=None)
    file_path: str = field(default=DEFAULT_VALUE)
    rating: float = field(default=None)
    type: str = field(default=None)


@dataclass
class FilmworkGenre(UUIDMixin):
    """Класс для представления жанра кинопроизведения."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    filmwork_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now())


@dataclass
class FilmworkPerson(UUIDMixin):
    """Класс для представления персоны кинопроизведения."""
    role: str = field(default=DEFAULT_VALUE)
    filmwork_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now())
