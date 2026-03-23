import streamlit as st
from datetime import datetime

class ChatInterface:
    def __init__(self):
        """Initialize the chat interface"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
    
    def display_chat(self):
        """Display the chat interface"""
        st.title("💬 Chat Interface")
        
        # Create a container for chat messages
        chat_container = st.container()
        
        # Display previous messages
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    st.caption(f"*{message['timestamp']}*")
        
        # Input section
        st.divider()
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            user_input = st.text_input(
                "Type your message:",
                placeholder="Enter your message here...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send", use_container_width=True)
        
        # Process message
        if send_button and user_input.strip():
            self.add_message("user", user_input)
            # Add a simple echo response for demo
            response = self.generate_response(user_input)
            self.add_message("assistant", response)
            st.rerun()
    
    def add_message(self, role, content):
        """Add a message to the chat history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        st.session_state.messages.append(message)
        st.session_state.chat_history.append(message)
    
    def generate_response(self, user_input):
        """Generate a simple response (can be replaced with actual AI)"""
        # Simple echo response for demo
        responses = {
            "hello": "Hi there! How can I help you today?",
            "help": "I'm here to assist you. Feel free to ask me anything!",
            "thanks": "You're welcome! Is there anything else you need?",
            "bye": "Goodbye! Have a great day!",
        }
        
        user_lower = user_input.lower().strip()
        for key, response in responses.items():
            if key in user_lower:
                return response
        
        return f"I received your message: '{user_input}'. How can I help you further?"
    
    def clear_history(self):
        """Clear chat history"""
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    def export_chat(self):
        """Export chat history as text"""
        if st.session_state.chat_history:
            chat_text = "\n".join([
                f"{msg['timestamp']} - {msg['role'].upper()}: {msg['content']}"
                for msg in st.session_state.chat_history
            ])
            return chat_text
        return "No chat history to export."


def main():
    """Main function to run the chat interface"""
    st.set_page_config(
        page_title="Chat Interface",
        page_icon="💬",
        layout="centered"
    )
    
    # Custom CSS styling for green and blue background with white text
    st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f766e 0%, #1e40af 100%);
            color: white;
        }
        .stMainBlockContainer {
            background: linear-gradient(135deg, #0f766e 0%, #1e40af 100%);
            color: white;
        }
        .stChatMessage {
            background-color: #059669;
            color: white;
            border-left: 5px solid #2563eb;
        }
        .stChatMessage[data-testid="chatAvatarIcon-user"] {
            background-color: #2563eb;
        }
        .stTextInput input {
            background-color: #10b981;
            color: white;
            border: 2px solid #2563eb;
            border-radius: 5px;
        }
        .stTextInput input::placeholder {
            color: #d1fae5;
        }
        .stButton button {
            background: linear-gradient(135deg, #059669 0%, #2563eb 100%);
            color: white;
            border: 2px solid white;
            font-weight: bold;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #047857 0%, #1e40af 100%);
        }
        .stTextArea textarea {
            background-color: #10b981;
            color: white;
            border: 2px solid #2563eb;
            border-radius: 5px;
        }
        .stTextArea textarea::placeholder {
            color: #d1fae5;
        }
        .stMarkdown {
            color: white;
        }
        .stDivider {
            border-color: #10b981;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f766e 0%, #1e40af 100%);
            color: white;
        }
        [data-testid="stSidebarContent"] {
            background: linear-gradient(180deg, #0f766e 0%, #1e40af 100%);
            color: white;
        }
        .stContainer {
            background: linear-gradient(135deg, #0f766e 0%, #1e40af 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with title and subtitle
    st.title("💬 HR Helpdesk Chat")
    st.markdown("<h4 style='color: #90caf9; text-align: center; margin-top: -10px;'>Your AI Assistant for HR Support</h4>", unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>⚙️ Controls</h2>", unsafe_allow_html=True)
        
        if st.button("Clear Chat History", use_container_width=True):
            chat.clear_history()
        
        if st.button("Export Chat", use_container_width=True):
            chat_text = chat.export_chat()
            st.text_area("Chat Export:", value=chat_text, height=200, disabled=True)
    
    # Initialize and display chat
    chat = ChatInterface()
    chat.display_chat()


if __name__ == "__main__":
    main()
