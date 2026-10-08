import streamlit as st
from google import genai

st.set_page_config(
    page_title="Masfa's AI",
    page_icon="🤖",
    layout="centered"
)

# =========================
# AI CLIENT
# =========================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================
# DESIGN
# =========================

st.html("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(38, 78, 125, 0.45),
            transparent 35%
        ),
        radial-gradient(
            circle at 85% 85%,
            rgba(7, 82, 78, 0.35),
            transparent 40%
        ),
        linear-gradient(
            145deg,
            #08152b 0%,
            #102b4d 45%,
            #073b3b 100%
        );

    color: white;
}


/* PAGE WIDTH */

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}


/* =========================
   TITLE
========================= */

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -1.5px;
    margin-bottom: 3px;
}


/* =========================
   SUBTITLE
========================= */

.subtitle {
    text-align: center;
    color: #c5d2df;
    font-size: 17px;
    margin-bottom: 15px;
}


/* =========================
   ONLINE STATUS
========================= */

.status {
    width: fit-content;
    margin: 0 auto 25px auto;

    padding: 7px 15px;

    border-radius: 30px;

    background: rgba(48, 211, 153, 0.10);

    border: 1px solid rgba(90, 220, 180, 0.25);

    color: #61ddb0;

    font-size: 13px;
    font-weight: 700;
}


/* =========================
   CHAT MESSAGES
========================= */

[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 13px;
    margin-bottom: 12px;
}


/* USER MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background: rgba(30, 55, 84, 0.75);

    border: 1px solid rgba(150, 190, 225, 0.12);

}


/* AI MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {

    background: rgba(8, 47, 53, 0.72);

    border: 1px solid rgba(90, 210, 190, 0.12);

}


/* =========================
   CHAT INPUT
========================= */

[data-testid="stChatInput"] {
    border-radius: 18px !important;
}


/* INPUT BOX */

[data-testid="stChatInput"] textarea {

    background: rgba(17, 29, 47, 0.95) !important;

    color: white !important;

    border: 1px solid #35516e !important;

    border-radius: 18px !important;

}


/* SEND BUTTON */

[data-testid="stChatInput"] button {

    background: #277f82 !important;

    border-radius: 13px !important;

}


/* =========================
   CLEAR CHAT
========================= */

button[kind="secondary"] {

    border-radius: 12px !important;

    border: 1px solid #36516c !important;

    background: rgba(255,255,255,0.05) !important;

    color: #d7e1eb !important;

}


/* =========================
   FOOTER
========================= */

.footer {

    text-align: center;

    color: #91a4b7;

    font-size: 12px;

    margin-top: 22px;

}

</style>
""")


# =========================
# HEADER
# =========================

st.html("""
<div class="main-title">
    🤖 Masfa's AI
</div>

<div class="subtitle">
    Your personal AI assistant
</div>

<div class="status">
    ● AI ONLINE
</div>
""")


# =========================
# CHAT MEMORY
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================
# CLEAR CHAT
# =========================

if st.button(
    "🗑️ Clear Chat",
    key="clear_chat"
):

    st.session_state.messages = []

    st.rerun()


# =========================
# SHOW OLD MESSAGES
# =========================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=(
            "🤖"
            if message["role"] == "assistant"
            else "👤"
        )
    ):

        st.write(
            message["content"]
        )


# =========================
# INPUT
# =========================

prompt = st.chat_input(
    "Ask Masfa's AI anything..."
)


# =========================
# USER MESSAGE
# =========================

if prompt:

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })


    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(prompt)


    # =========================
    # AI RESPONSE
    # =========================

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "Thinking..."
        ):

            response = client.models.generate_content(

                model="gemini-3.5-flash-lite",

                contents=f"""
You are Masfa's personal AI assistant.

Your creator is Masfa.

If the user asks who created you,
say: "I was created by Masfa."

If the user asks who Masfa is,
say: "She's the boss."

Be friendly, helpful, natural,
and concise.

Conversation:
{st.session_state.messages}

User:
{prompt}
"""
            )

            answer = response.text

            st.write(answer)


    # =========================
    # SAVE AI RESPONSE
    # =========================

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })


# =========================
# FOOTER
# =========================

st.html("""
<div class="footer">
    Made with 🤍 by Masfa
</div>
""")
