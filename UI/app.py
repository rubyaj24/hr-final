import streamlit as st
from login import show_login
from chat import show_chat

st.set_page_config(page_title="HR Helpdesk Agent", page_icon="💼")

# Initialize login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    show_chat()
else:
    show_login()