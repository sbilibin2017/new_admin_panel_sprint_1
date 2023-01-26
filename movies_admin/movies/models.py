import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex

# часто повторяющие параметры
DEFAULT_PARAMETERS = {'blank': True, 'null': True, 'default': ''}
# максимальная длина строкового поля
MAX_LENGTH = 255


class TimeStampedMixin(models.Model):
    '''Миксин для даты.'''

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    '''Миксин для id.'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    '''Класс для описания жанра.'''

    name = models.CharField(max_length=MAX_LENGTH, verbose_name=_('Name'))
    description = models.TextField(
        verbose_name=_('Description'), **DEFAULT_PARAMETERS)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    '''Класс для описания персоны.'''

    full_name = models.CharField(
        max_length=MAX_LENGTH, verbose_name=_('Full name'))

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    '''Класс для описания кинопроизведения.'''

    class FilmworkType(models.TextChoices):
        '''Класс для описания типа кинопроизведения.'''

        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'TV_show', _('TV show')

    title = models.CharField(max_length=MAX_LENGTH, verbose_name=_('Title'))
    description = models.TextField(
        verbose_name=_('Description'), **DEFAULT_PARAMETERS)
    creation_date = models.DateField(verbose_name=_(
        'Creation date'), blank=True, null=True)
    file_path = models.FileField(
        verbose_name=_('File path'), **DEFAULT_PARAMETERS)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Rating'), blank=True, null=True
    )
    type = models.CharField(
        max_length=MAX_LENGTH,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
        verbose_name=_('Type'),
    )

    genres = models.ManyToManyField(
        Genre, through='FilmworkGenre', verbose_name=_('Genres'))
    persons = models.ManyToManyField(
        Person, through='FilmworkPerson', verbose_name=_('Persons'))

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"filmwork"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class FilmworkGenre(UUIDMixin):
    '''Класс для описания жанров кинопроизведения.'''

    filmwork = models.ForeignKey(
        to='Filmwork', db_column='filmwork_id', on_delete=models.CASCADE, verbose_name=_('Filmwork')
    )
    genre = models.ForeignKey(to='Genre', db_column='genre_id',
                              on_delete=models.CASCADE, verbose_name=_('Genre'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return 'Жанры кинопроизведения'

    class Meta:
        db_table = "content\".\"filmwork_genre"
        verbose_name = _('FilmworkGenre')
        verbose_name_plural = _('FilmworkGenres')


class FilmworkPerson(UUIDMixin):
    '''Класс для описания персон кинопроизведения.'''

    filmwork = models.ForeignKey(
        to='Filmwork', db_column='filmwork_id', on_delete=models.CASCADE, verbose_name=_('Filmwork')
    )
    person = models.ForeignKey(to='Person', db_column='person_id',
                               on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.TextField(verbose_name=_('Role'), **DEFAULT_PARAMETERS)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return 'Персоны кинопроизведения'

    class Meta:
        indexes = [UniqueIndex(fields=['filmwork', 'person', 'role'])]
        db_table = "content\".\"filmwork_person"
        verbose_name = _('FilmworkPerson')
        verbose_name_plural = _('FilmworkPersons')
