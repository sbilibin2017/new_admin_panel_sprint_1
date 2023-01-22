CREATE SCHEMA IF NOT EXISTS content; 


SET search_path TO content,public;


ALTER ROLE app SET search_path TO content,public;


--
-- Create model Filmwork
--
CREATE TABLE "filmwork" ("created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "title" varchar(255) NOT NULL, "description" text NULL, "creation_date" date NULL, "file_path" varchar(100) NULL, "rating" double precision NULL, "type" varchar(255) NOT NULL);
--
-- Create model Genre
--
CREATE TABLE "genre" ("created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL, "description" text NULL);
--
-- Create model Person
--
CREATE TABLE "person" ("created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "full_name" varchar(255) NOT NULL);
--
-- Create model FilmworkPerson
--
CREATE TABLE "filmwork_person" ("id" uuid NOT NULL PRIMARY KEY, "role" text NULL, "created_at" timestamp with time zone NOT NULL, "filmwork_id" uuid NOT NULL, "person_id" uuid NOT NULL);
--
-- Create model FilmworkGenre
--
CREATE TABLE "filmwork_genre" ("id" uuid NOT NULL PRIMARY KEY, "created_at" timestamp with time zone NOT NULL, "filmwork_id" uuid NOT NULL, "genre_id" uuid NOT NULL);
--
-- Add field genres to filmwork
--
--
-- Add field persons to filmwork
--
--
-- Create index filmwork_pe_filmwor_425cc8_idx on field(s) filmwork, person, role of model filmworkperson
--
CREATE UNIQUE INDEX "filmwork_pe_filmwor_425cc8_idx" ON "filmwork_person" ("filmwork_id", "person_id", "role");
ALTER TABLE "filmwork_person" ADD CONSTRAINT "filmwork_person_filmwork_id_42e45666_fk_filmwork_id" FOREIGN KEY ("filmwork_id") REFERENCES "filmwork" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "filmwork_person" ADD CONSTRAINT "filmwork_person_person_id_db4693bd_fk_person_id" FOREIGN KEY ("person_id") REFERENCES "person" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "filmwork_person_filmwork_id_42e45666" ON "filmwork_person" ("filmwork_id");
CREATE INDEX "filmwork_person_person_id_db4693bd" ON "filmwork_person" ("person_id");
ALTER TABLE "filmwork_genre" ADD CONSTRAINT "filmwork_genre_filmwork_id_b6f5839b_fk_filmwork_id" FOREIGN KEY ("filmwork_id") REFERENCES "filmwork" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "filmwork_genre" ADD CONSTRAINT "filmwork_genre_genre_id_ad82d44a_fk_genre_id" FOREIGN KEY ("genre_id") REFERENCES "genre" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "filmwork_genre_filmwork_id_b6f5839b" ON "filmwork_genre" ("filmwork_id");
CREATE INDEX "filmwork_genre_genre_id_ad82d44a" ON "filmwork_genre" ("genre_id");


