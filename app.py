import streamlit as st
from google import genai

st.html("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
}

h1 {
    color: white;
    text-align: center;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px
    }
</style>
""")

st.title("🤖 Masfa's AI")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f"Your creator is Masfa. If asked who created you, say you were created by Masfa. If asked who Masfa is, say: 'She's the boss.'\n\nUser: {prompt}"
    )

    answer = response.text

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
