import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect("movie_booking.db")
    return conn

# Fetch all states
def get_states():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM states")
    states = cursor.fetchall()
    conn.close()
    return states

# Fetch cities for a given state_id
def get_cities(state_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM cities WHERE state_id=?", (state_id,))
    cities = cursor.fetchall()
    conn.close()
    return cities

# Fetch theatres for a given city_id
def get_theatres(city_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM theatres WHERE city_id=?", (city_id,))
    theatres = cursor.fetchall()
    conn.close()
    return theatres

# Fetch movies playing in a specific theatre
def get_movies_by_theatre(theatre_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, m.language, m.genre, s.show_time, s.available_seats
        FROM movie_shows s
        JOIN movies m ON s.movie_id = m.id
        WHERE s.theatre_id = ?
    """, (theatre_id,))
    movies = cursor.fetchall()
    conn.close()
    return movies

# Fetch show IDs by theatre (used for booking)
def get_show_ids_by_theatre(theatre_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, m.name, s.show_time, s.available_seats
        FROM movie_shows s
        JOIN movies m ON s.movie_id = m.id
        WHERE s.theatre_id = ?
    """, (theatre_id,))
    shows = cursor.fetchall()
    conn.close()
    return shows

# Book tickets and update seat availability
def book_tickets(user_id, show_id, num_tickets):
    conn = create_connection()
    cursor = conn.cursor()

    # Check current availability
    cursor.execute("SELECT available_seats FROM movie_shows WHERE id=?", (show_id,))
    result = cursor.fetchone()

    if result and result[0] >= num_tickets:
        new_seats = result[0] - num_tickets

        # Update available seats
        cursor.execute("UPDATE movie_shows SET available_seats=? WHERE id=?", (new_seats, show_id))

        # Log booking
        cursor.execute("""
            INSERT INTO bookings (user_id, show_id, num_tickets, booking_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, show_id, num_tickets, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()
        return True
def get_user_bookings(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, m.name, t.name, s.show_time, b.num_tickets, b.booking_time
        FROM bookings b
        JOIN movie_shows s ON b.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        WHERE b.user_id = ?
        ORDER BY b.booking_time DESC
    """, (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings