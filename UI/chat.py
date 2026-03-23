import streamlit as st

def show_chat():
    st.title("💼 HR Helpdesk Agent")

    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.clear()
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask your HR question...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("assistant"):
            response = f"(Demo Mode)\nRole: {st.session_state.role}\nQuestion: {user_input}"
            st.markdown(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )