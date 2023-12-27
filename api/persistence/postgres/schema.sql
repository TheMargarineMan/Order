
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    pass_hash bytea NOT NULL,
    salt TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS messages(
    id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    message TEXT,
    edited BOOLEAN,
    timestamp TIMESTAMP
)


