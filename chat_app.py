import streamlit as st
import requests
import json
import os

API_URL = "https://your-api-endpoint.com/reply"
CHAT_HISTORY_FILE = "chat_history.json"

def get_chatbot_response(user_input):
    """Send user input to the API and get the response."""
    return user_input
    response = requests.post(API_URL, json={"message": user_input})
    if response.status_code == 200:
        return response.json().get("reply", "Error: No response from API")
    return "Error: Failed to connect to API"

def load_chat_history():
    """Load chat history from a JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_chat_history(messages):
    """Save chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(messages, file)

query_params = st.query_params
if "logged_in" not in st.session_state:
    st.session_state.logged_in = query_params.get("logged_in", "false") == "true"

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if not st.session_state.logged_in:
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "password": 
            st.session_state.logged_in = True
            st.query_params["logged_in"] = "true"  
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()

st.title("Chat with Agent")
st.write("Ask anything and get a response!")

with st.sidebar:
    st.header("Chat History")
    if st.button("Upload File"):
        uploaded_file = st.file_uploader("", type=["txt", "pdf", "docx"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state.messages.append({"role": "user", "text": f"📂 {uploaded_file.name} uploaded!"})
            save_chat_history(st.session_state.messages)
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.query_params.clear()  
        os.remove(CHAT_HISTORY_FILE)  
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    bot_response = get_chatbot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "text": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    save_chat_history(st.session_state.messages)
