CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    state_id INTEGER,
    FOREIGN KEY (state_id) REFERENCES states(id)
);

CREATE TABLE IF NOT EXISTS theatres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    language TEXT,
    genre TEXT
);

CREATE TABLE IF NOT EXISTS movie_shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    theatre_id INTEGER,
    show_time TEXT,
    available_seats INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (theatre_id) REFERENCES theatres(id)
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    show_id INTEGER,
    num_tickets INTEGER,
    booking_time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES movie_shows(id)
);