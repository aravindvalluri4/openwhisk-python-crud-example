/* create table if not exists */
CREATE TABLE IF NOT EXISTS schemas
    (name varchar(100) PRIMARY KEY NOT NULL);

/* Some initial data */
INSERT INTO schemas VALUES ('pm')  ON CONFLICT DO NOTHING;
INSERT INTO schemas VALUES ('cowm')  ON CONFLICT DO NOTHING;
INSERT INTO schemas VALUES ('km')  ON CONFLICT DO NOTHING;
