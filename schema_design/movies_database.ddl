CREATE SCHEMA IF NOT EXISTS content; 


SET search_path TO content,public;


ALTER ROLE app SET search_path TO content,public;


CREATE TABLE filmwork (    
    'id' uuid NOT NULL PRIMARY KEY,
    'title' varchar(255) NOT NULL,
    'description' text NULL,
    'creation_date' date NULL, 
    'file_path' varchar(100) NULL, 
    'rating' double precision NULL, 
    'type' varchar(255) NOT NULL,
    'created_at' timestamp with time zone NOT NULL,
    'updated_at' timestamp with time zone NOT NULL
);
--
-- Create model Genre
--
CREATE TABLE genre (
    'id' uuid NOT NULL PRIMARY KEY,
    'name' varchar(255) NOT NULL,
    'description' text NULL
    'created_at' timestamp with time zone NOT NULL,
    'updated_at' timestamp with time zone NOT NULL 
);
--
-- Create model Person
--
CREATE TABLE person (
    'created_at' timestamp with time zone NOT NULL,
    'updated_at' timestamp with time zone NOT NULL,
    'id' uuid NOT NULL PRIMARY KEY,
    'full_name' varchar(255) NOT NULL
);

CREATE TABLE filmwork_person (
    'id' uuid NOT NULL PRIMARY KEY,     
    'filmwork_id' uuid NOT NULL, 
    'person_id' uuid NOT NULL,
    'role' text NULL, 
    'created_at' timestamp with time zone NOT NULL 
);

CREATE TABLE filmwork_genre (
    'id' uuid NOT NULL PRIMARY KEY,
    'filmwork_id' uuid NOT NULL, 
    'genre_id' uuid NOT NULL,
    'created_at' timestamp with time zone NOT NULL,
);

CREATE UNIQUE INDEX 'filmwork_person_role_idx'
    ON filmwork_person ('filmwork_id', 'person_id', 'role');
ALTER TABLE 'filmwork_person'
    ADD CONSTRAINT 'filmwork_person_filnwork_fk' 
    FOREIGN KEY ('filmwork_id') 
    REFERENCES filmwork ('id') DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE 'filmwork_person' 
    ADD CONSTRAINT 'filmwork_person_person_fk' 
    FOREIGN KEY ('person_id') 
    REFERENCES 'person' ('id') DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX 'filmwork_person_filmwork_idx' 
    ON filmwork_person ('filmwork_id');
CREATE INDEX 'filmwork_person_person_idx' 
    ON 'filmwork_person' ('person_id');
ALTER TABLE 'filmwork_genre' 
    ADD CONSTRAINT 'filmwork_genre_filmwork_fk' 
    FOREIGN KEY ('filmwork_id') 
    REFERENCES 'filmwork' ('id') DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE 'filmwork_genre' 
    ADD CONSTRAINT 'filmwork_genre_genre_fk' 
    FOREIGN KEY ('genre_id') 
    REFERENCES 'genre' ('id') DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX 'filmwork_genre_filmwork_idx' 
    ON 'filmwork_genre' ('filmwork_id');
CREATE INDEX 'filmwork_genre_genre_idx' 
    ON 'filmwork_genre' ('genre_id');

