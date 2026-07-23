import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Lehem AI", page_icon="🤖")
st.title("🤖 Lehem AI")
st.write("Aadarsh Ka Personal AI Assistant")

# API Setup
client = Groq(api_key="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")

# System Instruction (AI ka naam Lehem AI aur creator Aadarsh set kiya hai)
SYSTEM_INSTRUCTION = """
Tera naam 'Lehem AI' hai. Tu ek AI Assistant hai jise 'Aadarsh' ne banaya hai.
Jab bhi koi tujhse pooche ki:
- 'Tera naam kya hai?' ya 'Who are you?' -> Toh bolna: 'Mera naam Lehem AI hai.'
- 'Tujhe kisne banaya hai?' ya 'Who created you?' -> Toh bolna: 'Mujhe Aadarsh ne banaya hai! Aadarsh mera creator aur boss hai.'

Baaki sabhi sawalon ke jawab Hinglish mein friendly aur mast tarike se dena.
"""

# Session State Setup (Chat memory)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION}
    ]

# Screen par purani chat dikhana
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User ka input
if prompt := st.chat_input("Lehem AI se kuch bhi pucho..."):
    # 1. User message ko display aur save karo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI se response lo
    with st.chat_message("assistant"):
        with st.spinner("Lehem AI soch raha hai..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # AI response ko save karo
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")