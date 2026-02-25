import streamlit as st
from database import get_connection

def login():
    st.sidebar.title("Admin Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
           st.session_state.logged_in = True 
           st.rerun()
           st.sidebar.success("Login Successful")
        else:
            st.sidebar.error("Invalid username or password")