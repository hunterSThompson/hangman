CREATE TABLE IF NOT EXISTS Games (
    user_id TEXT CONSTRAINT games_pk PRIMARY KEY,
    word VARCHAR(100),
    letters VARCHAR(100),
    status BIT,
    lives INTEGER,
    guessed_letters VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(30) CONSTRAINT users_pk PRIMARY KEY,
    password VARCHAR(50),
    wins INTEGER,
    losses INTEGER
);