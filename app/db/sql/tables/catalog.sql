-- Table: public.catalogs

-- DROP TABLE IF EXISTS public."catalogs";

CREATE TABLE IF NOT EXISTS public."catalogs"
(
	id serial PRIMARY KEY,
	catalog_id uuid NOT NULL,
	catalog_name VARCHAR(255) NOT NULL,
	source VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP
);

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."catalogs"
    OWNER to postgres;

CREATE INDEX idx_catalog_id ON catalogs (catalog_id);
CREATE INDEX idx_catalogname ON catalogs (catalog_name);
