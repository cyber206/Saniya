
import streamlit as st
from src.Chatbot import Chatbot

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered"
)

# ---------------- PAGE STYLING ----------------

st.markdown("""
<style>
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        margin-bottom: 2rem;
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">AI Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Your personal AI assistant</div>',
    unsafe_allow_html=True
)

# ---------------- INITIALIZE CHATBOT ----------------

@st.cache_resource
def load_chatbot():
    return Chatbot()

try:
    bot = load_chatbot()
except Exception as e:
    st.error(f"Could not initialize chatbot: {e}")
    st.stop()

# ---------------- CHAT HISTORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("Settings")
    st.write("Chat with your AI assistant.")

    if st.button("Clear displayed chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Powered by Groq and PostgreSQL")

# ---------------- DISPLAY MESSAGES ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------

if prompt := st.chat_input("Type your message here..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = bot.chat(prompt)
                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
