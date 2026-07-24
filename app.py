import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Lehem AI", page_icon="🤖", layout="wide")

st.title("🤖 Lehem AI")
st.write("Aadarsh Ka Personal AI Assistant")

# System Instruction
SYSTEM_INSTRUCTION = """
Tera naam 'Lehem AI' hai. Tu ek AI Assistant hai jise 'Aadarsh' ne banaya hai.
Jab bhi koi tujhse pooche ki:
- 'Tera naam kya hai?' ya 'Who are you?' -> Toh bolna: 'Mera naam Lehem AI hai.'
- 'Tujhe kisne banaya hai?' ya 'Who created you?' -> Toh bolna: 'Mujhe Aadarsh ne banaya hai! Aadarsh mera creator aur boss hai.'
Baaki sabhi sawalon ke jawab Hinglish mein friendly aur mast tarike se dena.
"""

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
    login_option = st.sidebar.radio("Kaise use karna chahte ho?", ["Guest Mode", "Login Karo"])
    if login_option == "Login Karo":
        user_input = st.sidebar.text_input("Username")
        pass_input = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Log In"):
            if user_input:
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.sidebar.success(f"Welcome, {user_input}!")
                st.rerun()
            else:
                st.sidebar.error("Kripya username dalein!")
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
# Hardcoded Groq API Key
client = Groq(api_key="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")

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Display Chat History (Hide System Prompt)
for message in current_messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Lehem AI se kuch bhi pucho..."):
    # First message in this chat tab? Inject system prompt!
    if len(current_messages) == 0:
        current_messages.append({"role": "system", "content": SYSTEM_INSTRUCTION})

    # Save user message
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lehem AI soch raha hai..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in current_messages]
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
                # Save assistant response
                current_messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")
