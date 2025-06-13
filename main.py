import streamlit as st
from auth import signup_user, login_user
import database as db
import requests
from streamlit_lottie import st_lottie
import json
from pdf_ticket import generate_ticket_pdf_bytes 

# Streamlit page config
st.set_page_config(page_title="🎟 Movie Tix", page_icon="🎬")

# Load Lottie animation from file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_json = load_lottiefile("movie_lottie.json")
st_lottie(lottie_json, height=250, key="movie_header")

# Session init
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

# Header
st.title("🎬 Movie Tix")
st.markdown("---")

# Tabs for login/signup
auth_option = st.sidebar.radio("🔐 Authentication", ("Login", "Signup"))

# --- Signup ---
if auth_option == "Signup":
    st.subheader("📝 Create an Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not username or not email or not password:
            st.warning("⚠️ All fields are required!")
        else:
            if signup_user(username, email, password):
                st.success("✅ Account created! Please log in.")
            else:
                st.error("🚫 Username or Email already exists.")

# --- Login ---
else:
    st.subheader("🔑 Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("⚠️ All fields are required!")
        else:
            user_id = login_user(email, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.success("🎉 Login successful!")
            else:
                st.error("🚫 Invalid email or password.")

# --- Dashboard After Login ---
if st.session_state.logged_in:
    st.success("✅ Logged in successfully!")

    st.subheader("📍 Choose Your Location")
    st.markdown("---")

    # Fetch states
    states = db.get_states()
    if states:
        state_dict = {name: sid for sid, name in states}
        selected_state = st.selectbox("Choose State", list(state_dict.keys()))

        if selected_state:
            cities = db.get_cities(state_dict[selected_state])
            if cities:
                city_dict = {name: cid for cid, name in cities}
                selected_city = st.selectbox("Choose City", list(city_dict.keys()))

                if selected_city:
                    theatres = db.get_theatres(city_dict[selected_city])
                    if theatres:
                        theatre_dict = {name: tid for tid, name in theatres}
                        selected_theatre = st.selectbox("Choose Theatre", list(theatre_dict.keys()))

                        if selected_theatre:
                            st.markdown("### 🎞 Available Shows")
                            shows = db.get_show_ids_by_theatre(theatre_dict[selected_theatre])

                            if shows:
                                show_options = {f"{m} - {time} ({seats} seats left)": sid for sid, m, time, seats in shows}
                                selected_show = st.selectbox("🎬 Select a Show", list(show_options.keys()))

                                num_tickets = st.number_input("🎟 Number of Tickets", min_value=1, step=1)

                                if st.button("✅ Book Tickets"):
                                    show_id = show_options[selected_show]
                                    success = db.book_tickets(st.session_state.user_id, show_id, num_tickets)

                                    if success:
                                        st.success("🎉 Booking Confirmed!")
                                    else:
                                        st.error("❌ Not enough seats available.")
                            else:
                                st.info("ℹ️ No shows available.")
                    else:
                        st.warning("⚠️ No theatres in this city.")
            else:
                st.warning("⚠️ No cities in this state.")
    else:
        st.warning("⚠️ No states found. Please load the data.")

    # --- Booking History + PDF Download ---
    st.markdown("---")
    st.subheader("📜 Booking History")

    bookings = db.get_user_bookings(st.session_state.user_id)

    if bookings:
        for booking_id, movie, theatre, show_time, num_tickets, booking_time in bookings:
            with st.expander(f"🎬 {movie} at {theatre}"):
                st.write(f"Show Time: {show_time}")
                st.write(f"Tickets Booked: {num_tickets}")
                st.write(f"Booking Time: {booking_time}")

                pdf_filename = f"ticket_{booking_id}.pdf"

                if st.button(f"🧾 Generate Ticket #{booking_id}", key=f"gen_{booking_id}"):
                    pdf_bytes = generate_ticket_pdf_bytes(
                        booking_id, movie, theatre, show_time, num_tickets
                    )
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name=f"ticket_{booking_id}.pdf",
                        mime="application/pdf",
                        key=f"dl_{booking_id}"
                    )    
        else:
            st.info("You have no bookings yet.")