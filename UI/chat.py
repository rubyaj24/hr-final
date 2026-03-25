"""Chat interface for HR Helpdesk."""

import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/ask")


def show_chat():
    """Display the chat interface."""
    st.title("HR Helpdesk Agent")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask your HR question...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"query": user_input},
                        timeout=60,
                    )
                    response.raise_for_status()
                    result = response.json()
                    answer = result.get("answer", "No answer found.")
                except requests.exceptions.RequestException as e:
                    answer = f"Error: Could not connect to server. Is the API running?\n\nDetails: {str(e)}"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    st.set_page_config(page_title="HR Helpdesk", page_icon="HR")
    show_chat()
