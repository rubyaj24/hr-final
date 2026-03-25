import streamlit as st
import requests

st.title("Chatbot")

user_input = st.text_input("Enter your message:")

if user_input:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"query": user_input}
        )
        response.raise_for_status()
        result = response.json()

        content = result.get("content", "") if isinstance(result, dict) else ""
        if "<bot>:" in content:
            display_text = content.split("<bot>:", 1)[1].strip()
        else:
            display_text = content.strip() or "No relevant response found."

        st.write("**Response:**")
        st.write(display_text)
    except Exception as e:
        st.error(f"Error: {str(e)}")