-- Runs automatically on first container start
-- (mounted into /docker-entrypoint-initdb.d/ by docker-compose)

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);
