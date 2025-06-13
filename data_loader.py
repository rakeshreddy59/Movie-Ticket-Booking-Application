import sqlite3

conn = sqlite3.connect("movie_booking.db")
cursor = conn.cursor()

# --- Insert States ---
states = [("Andhra Pradesh",), ("Telangana",), ("Karnataka",)]
cursor.executemany("INSERT INTO states (name) VALUES (?)", states)

# --- Insert Cities ---
cities = [
    ("Visakhapatnam", 1),
    ("Vijayawada", 1),
    ("Hyderabad", 2),
    ("Warangal", 2),
    ("Bangalore", 3),
]
cursor.executemany("INSERT INTO cities (name, state_id) VALUES (?, ?)", cities)

# --- Insert Theatres ---
theatres = [
    ("INOX CMR Central", 1),
    ("PVR Mangalagiri", 2),
    ("Prasads IMAX", 3),
    ("Asian Multiplex", 4),
    ("PVR Orion Mall", 5),
]
cursor.executemany("INSERT INTO theatres (name, city_id) VALUES (?, ?)", theatres)

# --- Insert Movies ---
movies = [
    ("Salaar", "Telugu", "Action"),
    ("Animal", "Hindi", "Thriller"),
    ("Jawan", "Hindi", "Drama"),
    ("Sita Ramam", "Telugu", "Romance"),
    ("Leo", "Tamil", "Action"),
]
cursor.executemany("INSERT INTO movies (name, language, genre) VALUES (?, ?, ?)", movies)

# --- Insert Movie Shows ---
movie_shows = [
    (1, 1, "2025-04-19 18:00", 50),
    (2, 2, "2025-04-19 21:00", 60),
    (3, 3, "2025-04-20 17:30", 45),
    (4, 4, "2025-04-20 20:00", 30),
    (5, 5, "2025-04-21 19:00", 40),
]
cursor.executemany("""
    INSERT INTO movie_shows (movie_id, theatre_id, show_time, available_seats)
    VALUES (?, ?, ?, ?)
""", movie_shows)

conn.commit()
conn.close()

print("✅ Dummy data inserted successfully.")