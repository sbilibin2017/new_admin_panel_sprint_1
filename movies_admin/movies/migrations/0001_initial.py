'''Миграции.'''

import uuid

import django.core.validators
import django.db.models.deletion
import psqlextra.indexes.unique_index
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(
                    auto_now=True, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True,
                 default='', null=True, verbose_name='Description')),
                ('creation_date', models.DateField(
                    blank=True, null=True, verbose_name='Creation date')),
                ('file_path', models.FileField(blank=True, default='',
                 null=True, upload_to='', verbose_name='File path')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(
                    0), django.core.validators.MaxValueValidator(100)], verbose_name='Rating')),
                ('type', models.CharField(choices=[('movie', 'Movie'), (
                    'TV_show', 'TV show')], default='movie', max_length=255, verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Filmwork',
                'verbose_name_plural': 'Filmworks',
                'db_table': 'content"."filmwork',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(
                    auto_now=True, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True,
                 default='', null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(
                    auto_now=True, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(
                    max_length=255, verbose_name='Full name')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='FilmworkPerson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(blank=True,
                 default='', null=True, verbose_name='Role')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created at')),
                ('filmwork', models.ForeignKey(db_column='filmwork_id',
                 on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='Filmwork')),
                ('person', models.ForeignKey(db_column='person_id',
                 on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='Person')),
            ],
            options={
                'verbose_name': 'FilmworkPerson',
                'verbose_name_plural': 'FilmworkPersons',
                'db_table': 'content"."filmwork_person',
            },
        ),
        migrations.CreateModel(
            name='FilmworkGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created at')),
                ('filmwork', models.ForeignKey(db_column='filmwork_id',
                 on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='Filmwork')),
                ('genre', models.ForeignKey(db_column='genre_id',
                 on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='Genre')),
            ],
            options={
                'verbose_name': 'FilmworkGenre',
                'verbose_name_plural': 'FilmworkGenres',
                'db_table': 'content"."filmwork_genre',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(
                through='movies.FilmworkGenre', to='movies.Genre', verbose_name='Genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(
                through='movies.FilmworkPerson', to='movies.Person', verbose_name='Persons'),
        ),
        migrations.AddIndex(
            model_name='filmworkperson',
            index=psqlextra.indexes.unique_index.UniqueIndex(
                fields=['filmwork', 'person', 'role'], name='filmwork_pe_filmwor_425cc8_idx'),
        ),
    ]
