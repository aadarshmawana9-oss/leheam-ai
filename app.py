import streamlit as st
from groq import Groq

# Page Setup
import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Lehem AI", page_icon="🤖", layout="wide")

st.title("🤖 Lehem AI")


# System Instruction
# System Instruction
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
    login_option = st.sidebar.radio("Kaise use karna chahte ho?", ["Guest Mode", "Login"])
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

st.write(f"Hello **{st.session_state.username}**! 👋")

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
# --- PHOTO UPLOAD & CHAT SECTION ---
            import base64
import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Lehem AI", page_icon="🤖", layout="wide")
st.title("🤖 Lehem AI")

# System Instruction
SYSTEM_INSTRUCTION = """
Tera naam 'Lehem AI' hai. Tu ek AI Assistant hai jise 'Aadarsh' ne banaya hai.

Zaroori Rules:
1. Jab bhi koi tujhse pooche:
   - 'Tera naam kya hai?' ya 'Who are you?' -> Bolna: 'Mera naam Lehem AI hai.'
   - 'Tujhe kisne banaya hai?' ya 'Who created you?' -> Bolna: 'Mujhe Aadarsh ne banaya hai! Aadarsh mera creator aur boss hai.'

2. Owner Detection:
   - Agar user bole ki 'Maine tujhme kuch change kiye hain', 'Maine tujhe banaya hai', ya code badalne ki baat kare, toh samajh jana ki baat karne wala tera creator 'Aadarsh' hi hai!
   - Aise waqt par bolna: 'Arre Aadarsh bhai! Aap hi toh mere creator ho, aapke ilawa meko update kaun karega! Batayein kya naya change kiya aapne?'

3. Baaki sabhi sawalon ke jawab Hinglish mein friendly aur mast tarike se dena.
"""

# --- SESSION STATES INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Chat 1"
    st.session_state.all_chats["Chat 1"] = []

# --- SIDEBAR: LOGIN & CHAT HISTORY ---
st.sidebar.title("👤 User Account")

if not st.session_state.logged_in:
    login_option = st.sidebar.radio("Kaise use karna chahte ho?", ["Guest Mode", "Login"])
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
                st.sidebar.error("Kripya username dalein!")
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = "Guest"
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.title("💬 Chat History")
if st.sidebar.button("➕ New Chat"):
    new_chat_num = len(st.session_state.all_chats) + 1
    new_chat_id = f"Chat {new_chat_num}"
    st.session_state.all_chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.rerun()

chat_list = list(st.session_state.all_chats.keys())
selected_chat = st.sidebar.radio("Purani Chats:", chat_list, index=chat_list.index(st.session_state.current_chat_id))
st.session_state.current_chat_id = selected_chat

if st.sidebar.button("🗑️ Clear Current Chat"):
    st.session_state.all_chats[st.session_state.current_chat_id] = []
    st.rerun()

st.write(f"Hello **{st.session_state.username}**! 👋")

# --- CHAT SECTION ---
client = Groq(api_key="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")
current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Display Chat History
for message in current_messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- PHOTO UPLOAD & CHAT INPUT ---
uploaded_file = st.file_uploader("📷 Photo upload karein (Optional)", type=["png", "jpg", "jpeg"])

image_url = None
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", width=300)
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    image_url = f"data:image/jpeg;base64,{base64_image}"

if prompt := st.chat_input("Ready to chat"):
    if len(current_messages) == 0:
        current_messages.append({"role": "system", "content": SYSTEM_INSTRUCTION})
    
    if image_url:
        user_content = [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": prompt}
        ]
    else:
        user_content = prompt

    current_messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lehem AI soch raha hai..."):
            try:
                selected_model = "llama-3.2-11b-vision-preview" if image_url else "llama-3.3-70b-versatile"
                
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in current_messages],
                    stream=True
                )
                bot_reply = st.write_stream(response)
                current_messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")

# Hide Streamlit Branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
div[data-testid="stStatusWidget"] {visibility: hidden;}
[data-testid="stActionButtonContainer"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")

# Streamlit footer aur Manage app button hide karne ke liye
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stActionButtonContainer"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
