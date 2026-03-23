import streamlit as st

# Dummy users (replace with DB later)
USERS = {
    "employee1": {"password": "1234", "role": "Employee"},
    "manager1": {"password": "1234", "role": "Manager"},
    "hradmin": {"password": "admin123", "role": "HR Admin"},
}

def show_login():
    st.title("🔐 HR Helpdesk Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")