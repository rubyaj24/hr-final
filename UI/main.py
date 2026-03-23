import streamlit as st
import requests

st.title("Chatbot")

user_input = st.text_input("Enter your message:")

if user_input:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/retrieve",
            json={"query": user_input}
        )
        result = response.json()
        st.write("**Response:**")
        st.write(result)
    except Exception as e:
        st.error(f"Error: {str(e)}")