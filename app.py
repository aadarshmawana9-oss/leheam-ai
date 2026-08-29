import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Ram AI", page_icon="🤖", layout="wide")

st.title("🤖Ram AI")
st.write("AI Assistant")

# System Instruction / Persona
SYSTEM_INSTRUCTION = """
Tera naam 'Ram AI' hai. Tu ek AI Assistant hai jise 'Aadarsh' ne banaya hai.
Jab bhi koi tujhse pooche ki:
- 'Tera naam kya hai?' ya 'Who are you?' -> Toh bolna: 'Mera naam Ram AI hai.'
- 'Tujhe kisne banaya hai?' ya 'Who created you?' -> Toh bolna: 'Mujhe Aadarsh jo ki Sunit kumar ka aur Preeti ka beta hai unhone banaya hai! Aadarsh mera creator aur boss hai.'
Baaki sabhi sawalon ke jawab Hinglish mein friendly aur mast tarike se dena.
"""

# --- CONFIGURE GEMINI API ---
genai.configure(api_key="AQ.Ab8RN6LqNjNPuTzEr8sLsyRI5NU1xF7lfoHaBEu6CB68cYOAIg")

# Initialize Gemini Model with System Instruction
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

# --- SESSION STATES INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}  # History store karne ke liye
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Chat 1"
    st.session_state.all_chats["Chat 1"] = []

# --- SIDEBAR: LOGIN & CHAT HISTORY ---
st.sidebar.title("👤 User Account")

# Login / Guest Option
if not st.session_state.logged_in:
    login_option = st.sidebar.radio("how do you want to use it ?", ["Guest Mode", "Login"])
    if login_option == "Login":
        user_input = st.sidebar.text_input("Username")
        pass_input = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Log In"):
            if user_input:
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.sidebar.success(f"Welcome, {user_input}!")
                st.rerun()
            else:
                st.sidebar.error("enter username!")
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = "Guest"
        st.rerun()

st.sidebar.markdown("---")

# --- NEW CHAT BUTTON & HISTORY ---
st.sidebar.title("💬 Chat History")

if st.sidebar.button("➕ New Chat"):
    new_chat_num = len(st.session_state.all_chats) + 1
    new_chat_id = f"Chat {new_chat_num}"
    st.session_state.all_chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.rerun()

# Previous Chats List
chat_list = list(st.session_state.all_chats.keys())
selected_chat = st.sidebar.radio(
    "Purani Chats:", 
    chat_list, 
    index=chat_list.index(st.session_state.current_chat_id)
)
st.session_state.current_chat_id = selected_chat

# Clear Current Chat Option
if st.sidebar.button("🗑️ Clear Current Chat"):
    st.session_state.all_chats[st.session_state.current_chat_id] = []
    st.rerun()

st.write(f"Hello **{st.session_state.username}**! 👋 Tum **{st.session_state.current_chat_id}** mein ho.")

# --- CHAT SECTION ---
current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Display Chat History
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask anything to Ram AI..."):
    # Save user message
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ram AI is thinking..."):
            try:
                # Format chat history for Gemini
                gemini_history = []
                for m in current_messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [m["content"]]})
                
                chat_session = model.start_chat(history=gemini_history)
                response = chat_session.send_message(prompt)
                bot_reply = response.text
                
                st.markdown(bot_reply)
                # Save assistant response
                current_messages.append({"role": "model", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")
