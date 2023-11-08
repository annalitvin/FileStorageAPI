-- Table: public.files

-- DROP TABLE IF EXISTS public."files";

CREATE TABLE IF NOT EXISTS public."files"
(
	id serial PRIMARY KEY,
	file_id uuid NOT NULL,
	catalog_id serial NOT NULL,
	file_name VARCHAR ( 150 ) NOT NULL UNIQUE,
	content_type VARCHAR ( 150 ) NOT NULL,
	file_size INT NOT NULL CHECK(file_size > 0),
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP,
	CONSTRAINT fk_catalogs
      FOREIGN KEY (catalog_id)
	  REFERENCES catalogs(id)
);

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."files"
    OWNER to postgres;

CREATE INDEX idx_file_id ON files (file_id);
CREATE INDEX idx_filename ON files (file_name);
