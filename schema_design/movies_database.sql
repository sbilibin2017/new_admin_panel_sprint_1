-- создаем схему
BEGIN;
CREATE SCHEMA IF NOT EXISTS "content";

-- помещаем созданную схему в корень
SET search_path TO "content","public";

-- жанры
CREATE TABLE IF NOT EXISTS "genre"(
    id uuid primary key,
    name varchar(128) not null,
    description text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- персоны
CREATE TABLE IF NOT EXISTS "person"( 
    id uuid primary key,
    full_name varchar(128) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- кинопроизведения
CREATE TABLE IF NOT EXISTS "filmwork"(
    id uuid primary key,
    title varchar(128) not null,
    description text,
    creation_date date,
    file_path varchar(128),
    rating float,
    type varchar(128) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- жанры кинопроизведений
CREATE TABLE IF NOT EXISTS "filmwork_genre"(
    id uuid primary key,
    filmwork_id uuid not null,
    genre_id uuid not null,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX filmwork_genre_idx 
    ON "filmwork_genre" (filmwork_id, genre_id);

-- персоны кинопроизведений
CREATE TABLE IF NOT EXISTS "filmwork_person"(
    id uuid primary key,
    filmwork_id uuid not null,
    person_id uuid not null,
    role varchar(128) not null,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX filmwork_person_role_idx 
    ON "filmwork_person" (filmwork_id, person_id, role);

COMMIT;