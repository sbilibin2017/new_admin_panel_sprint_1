CREATE SCHEMA IF NOT EXISTS content; 


SET search_path TO content,public;


ALTER ROLE app SET search_path TO content,public;


CREATE TABLE IF NOT EXISTS filmwork ( 
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);
CREATE INDEX filmwork_creation_date_rating_idx 
    ON filmwork(creation_date, rating); 


CREATE TABLE IF NOT EXISTS genre (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


CREATE TABLE IF NOT EXISTS person( 
    id text primary key, 
    full_name text not null, 
    created_at timestamp with time zone, 
    updated_at timestamp with time zone
);


CREATE TABLE IF NOT EXISTS filmwork_genre (
    id TEXT PRIMARY KEY,
    film_work_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX filmwork_genre_idx 
    ON filmwork_genre (film_work_id, genre_id);


CREATE TABLE IF NOT EXISTS filmwork_person (
    id TEXT PRIMARY KEY,
    film_work_id TEXT NOT NULL,
    person_id TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX filmwork_person_role_idx 
    ON person_film_work (filmwork_id, person_id, role);
