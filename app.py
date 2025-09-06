import streamlit as st
from bible_utils import fetch_verse
from llm_utils import explain_verse
import re
import random
import time

st.set_page_config(page_title="Bible Chat Assistant", layout="wide")

# ---------------- CSS Styling ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #faf6f3, #e8d9c5);
    font-family: 'Georgia', serif;
    color: #2d2d2d;
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translate(-50%, -20%);
    background: url('https://upload.wikimedia.org/wikipedia/commons/7/79/Christian_cross.svg') no-repeat center;
    background-size: 250px;
    opacity: 0.06;
    z-index: 0;
    width: 100%;
    height: 100%;
}

h1 {
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
    color: #4b2e2e !important;
    text-align: center;
    font-size: 2.7em;
    margin-bottom: 15px;
}

.chat-user {
    background-color: #edf2fb;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: right;
    border: 1px solid #c8d6e5;
}
.chat-bot {
    background-color: #fff8e7;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid #e0c097;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
}
.input-center {
    display: flex;
    justify-content: center;
    margin-top: 150px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Creative Sidebar ----------------
daily_verses = [
    "Psalm 119:105 – *Your word is a lamp to my feet and a light to my path.*",
    "Isaiah 40:31 – *They that wait upon the Lord shall renew their strength.*",
    "John 14:6 – *I am the way, and the truth, and the life.*",
    "Proverbs 3:5 – *Trust in the Lord with all your heart.*",
]
quotes = [
    "🌿 *'Be still, and know that I am God.'* – Psalm 46:10",
    "🕊 *'The Lord is my shepherd; I shall not want.'* – Psalm 23:1",
    "✝ *'Love one another as I have loved you.'* – John 15:12",
    "📖 *'Iron sharpens iron, so one person sharpens another.'* – Proverbs 27:17",
]


st.sidebar.markdown("## 🌿 Daily Verse")
st.sidebar.markdown(random.choice(daily_verses))

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Biblical Thought")
st.sidebar.markdown(random.choice(quotes))

st.sidebar.markdown("---")
st.sidebar.info("💡 *Ask me about any Bible verse or a topic. I'll explain with love and scripture.*")

# ---------------- Greeting Screen ----------------
if "greeted" not in st.session_state:
    st.session_state["greeted"] = False

if not st.session_state["greeted"]:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align:center;'> Hello, Beloved of God </h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:20px;'>Welcome to your Bible Companion. May the Word guide your steps today. ✝️</p>", unsafe_allow_html=True)
        

    time.sleep(5)  # Show greeting for 3 seconds
    placeholder.empty()  # Cleanly remove greeting
    st.session_state["greeted"] = True

# ---------------- Chat Logic ----------------
st.markdown("""
    <div style='text-align: center; padding: 30px; 
                background: linear-gradient(90deg, #fff8e7, #f9f3e9); 
                border-radius: 15px; 
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>
        <h1 style='color:#4b2e2e; font-size: 3em; margin-bottom: 0;'> The Word Companion ✝️</h1>
        <p style='font-size: 20px; color:#555; font-style: italic; margin-top: 10px;'>
            An AI friend to walk with God
        </p>
    </div>
""", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def is_verse_reference(text):
    return re.match(r"^[1-3]?\s?[A-Za-z]+\s\d+:\d+$", text.strip())

# Center input when no messages, move to top after first query
if len(st.session_state['messages']) == 0:
    with st.container():
        st.markdown("<div class='input-center'>", unsafe_allow_html=True)
        user_input = st.text_input("Ask, and it shall be given you — What would you like to explore?", "", key="input_center")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    user_input = st.text_input("Ask, and it shall be given you — What would you like to explore?", "", key="input_top")

# Handle input
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})

    if is_verse_reference(user_input):
        verse_text = fetch_verse(user_input)
        explanation = explain_verse(verse_text)
        st.session_state['messages'].append({"role": "bot", "content": f"📖 **{verse_text}**\n\n{explanation}"})
    else:
        explanation = explain_verse("", question=user_input)
        st.session_state['messages'].append({"role": "bot", "content": explanation})

# Display messages
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"<div class='chat-user'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bot'><strong>BibleBot:</strong> {msg['content']}</div>", unsafe_allow_html=True)
