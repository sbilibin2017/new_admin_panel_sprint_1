-- создаем схему
BEGIN;
CREATE SCHEMA IF NOT EXISTS "content";

-- помещаем созданную схему в корень
SET search_path TO "content","public";

-- жанры
CREATE TABLE IF NOT EXISTS "genre"(
    id UUID PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- персоны
CREATE TABLE IF NOT EXISTS "person"( 
    id UUID PRIMARY KEY,
    full_name VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- кинопроизведения
CREATE TABLE IF NOT EXISTS "filmwork"(
    id UUID PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    creation_date date,
    file_path VARCHAR(128),
    rating FLOAT,
    type VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- жанры кинопроизведений
CREATE TABLE IF NOT EXISTS "filmwork_genre"(
    id UUID PRIMARY KEY,
    filmwork_id UUID NOT NULL,
    genre_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE
);
CREATE UNIQUE INDEX filmwork_genre_idx 
    ON "filmwork_genre" (filmwork_id, genre_id);

-- персоны кинопроизведений
CREATE TABLE IF NOT EXISTS "filmwork_person"(
    id UUID PRIMARY KEY,
    filmwork_id UUID NOT NULL,
    person_id UUID NOT NULL,
    role VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE
);
CREATE UNIQUE INDEX filmwork_person_role_idx 
    ON "filmwork_person" (filmwork_id, person_id, role);

COMMIT;