import streamlit as st
from groq import Groq

# 1. Page Configuration Setup
st.set_page_config(page_title="Lehem AI", page_icon="🤖", layout="centered")
st.title("🤖 Lehem AI")
st.write("Aadarsh Ka Personal AI Assistant")

# 2. Secure API & Client Initialization 
# Tip: Code bechte ya share karte waqt is key ko .streamlit/secrets.toml me shift kar dena
api_key_str = "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".strip()
client = Groq(api_key=api_key_str)

# 3. System Instructions (AI ki basic identity aur guidelines)
SYSTEM_INSTRUCTION = """
Tera naam 'Lehem AI' hai. Tu ek AI Assistant hai jise 'Aadarsh' ne banaya hai.
Jab bhi koi tujhse pooche ki:
- 'Tera naam kya hai?' ya 'Who are you?' -> Toh bolna: 'Mera naam Lehem AI hai.'
- 'Tujhe kisne banaya hai?' ya 'Who created you?' -> Toh bolna: 'Mujhe Aadarsh ne banaya hai! Aadarsh mera creator aur boss hai.'

Baaki sabhi sawalon ke jawab Hinglish mein friendly, short aur mast tarike se dena.
"""

# 4. Session State Init (Keval chat messages ke liye taaki UI clean rahe)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Render Visible Chat History on Screen
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input Catch & Process Loop
if prompt := st.chat_input("Lehem AI se kuch bhi pucho..."):
    # User message ko display aur save karo
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Runtime Block
    with st.chat_message("assistant"):
        with st.spinner("Lehem AI soch raha hai..."):
            try:
                # System prompt ko har dynamic request ke zero index par prepend karo
                api_payload = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + st.session_state.chat_history
                
                # Groq Chat Completion Endpoint Call - MODEL CHANGED TO STABLE VERSION
                response = client.chat.completions.create(
                    model="llama-3.3-70b-specdec",
                    messages=api_payload,
                    temperature=0.7
                )
                
                # Sahi object structure parsing syntax
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # Assistant message state backend me append karo
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Error aaya bhai: {e}")
