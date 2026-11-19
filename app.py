
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Step 1: Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Step 2: Check API key
if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

# Step 3: Connect with Gemini
client = genai.Client(api_key=api_key)

# Step 4: Custom AI instructions
SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer questions clearly and professionally.
Use simple language.
Provide examples whenever necessary.
"""

# Step 5: Configure Streamlit page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

h1 {
    color: #1e293b;
    text-align: center;
}

.stCaption {
    text-align: center;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.stButton button {
    border-radius: 10px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# Step 6: Chatbot heading
st.title("🤖 Gemini AI Assistant")
st.caption("Your intelligent AI-powered personal assistant")
st.divider()

# Step 7: Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Step 8: Welcome message
if not st.session_state.messages:
    st.info(
        "👋 Hello! I am your Gemini AI Assistant. "
        "Ask me anything to get started."
    )

# Step 9: Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Step 10: Sidebar information
st.sidebar.title("🤖 AI Assistant")

st.sidebar.info(
    "Powered by Google Gemini"
)

st.sidebar.subheader("Features")

st.sidebar.write("💬 Interactive Chat")
st.sidebar.write("🧠 Conversation Memory")
st.sidebar.write("⚙️ Custom Instructions")
st.sidebar.write("🗑️ Clear Chat")
st.sidebar.subheader("Chatbot Settings")

temperature = st.sidebar.slider(
    "Response Creativity",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

st.sidebar.divider()

st.sidebar.subheader("Chat Statistics")

st.sidebar.write(
    "User Messages:",
    sum(
        1 for m in st.session_state.messages
        if m["role"] == "user"
    )
)

st.sidebar.write(
    "AI Responses:",
    sum(
        1 for m in st.session_state.messages
        if m["role"] == "assistant"
    )
)

# Step 11: Message counter
st.sidebar.metric(
    "Total Messages",
    len(st.session_state.messages)
)

# Step 12: Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step 13: Chat input
user_input = st.chat_input("Ask me anything...")

# Step 14: Process user question
if user_input:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Step 15: Generate Gemini response
    try:
        with st.spinner("🤖 Gemini is thinking..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash",

                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "temperature": temperature
                },

                contents=[
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ]
            )

        bot_response = response.text or "No response generated."

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        bot_response = None

    # Step 16: Save and display AI response
    if bot_response:

        st.session_state.messages.append(
            {"role": "assistant", "content": bot_response}
        )

        with st.chat_message("assistant"):
            st.markdown(bot_response)

st.divider()

st.markdown(
    "<center>Developed using Python, Streamlit and Gemini AI</center>",
    unsafe_allow_html=True
)


