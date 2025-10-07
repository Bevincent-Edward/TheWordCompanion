import streamlit as st
from bible_utils import fetch_verse
from llm_utils import explain_verse
import re
import random
import time
import os

st.set_page_config(page_title="Bible Chat Assistant", layout="wide")

# ---------------- Initialization Section ----------------
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if "greeted" not in st.session_state:
    st.session_state["greeted"] = False

# Function to load external CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file at the beginning of the script
load_css("style.css")

# ---------------- Creative Sidebar ----------------
daily_verses = [
    "Psalm 119:105 – *Your word is a lamp to my feet and a light to my path.*",
    "Isaiah 40:31 – *They that wait upon the Lord shall renew their strength.*",
    "John 14:6 – *I am the way, and the truth, and the life.*",
    "Proverbs 3:5 – *Trust in the Lord with all your heart.*",
    "John 3:16 – *For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.*",
    "Ephesians 2:8-9 – *For it is by grace you have been saved, through faith—and this not from yourselves, it is the gift of God—not by works, so that no one can boast.*",
    "Romans 5:8 – *But God shows his love for us in that while we were still sinners, Christ died for us.*",
    "1 John 4:10 – *In this is love, not that we have loved God but that he loved us and sent his Son to be the propitiation for our sins.*",
    "2 Corinthians 5:17 – *Therefore, if anyone is in Christ, he is a new creation; the old has passed away, behold, the new has come.*",
    "Romans 8:38-39 – *For I am sure that neither death nor life, nor angels nor rulers, nor things present nor things to come, nor powers, nor height nor depth, nor anything else in all creation, will be able to separate us from the love of God in Christ Jesus our Lord.*",
    "John 15:13 – *Greater love has no one than this, that someone lay down his life for his friends.*",
]

st.sidebar.markdown("## 🌿 Daily Verse")
st.sidebar.markdown(random.choice(daily_verses))

st.sidebar.markdown("---")
st.sidebar.markdown("### A Heavenly Reminder ❤️ ")
st.sidebar.markdown("Jesus loves you. He died for your sins and rose on the third day. Repent, for the Kingdom of Heaven is near.")

st.sidebar.markdown("---")
st.sidebar.info("💡 *Ask me about any Bible verse or a topic. I'll explain with love and scripture.*")
st.sidebar.caption("Developed by Bevin, A Servant of God")


# ---------------- Greeting Screen ----------------
if not st.session_state["greeted"]:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align:center;'> Hello, Beloved of God </h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:20px;'>Welcome to your Bible Companion. May the Word guide your steps today. ✝️</p>", unsafe_allow_html=True)

    time.sleep(5)
    placeholder.empty()
    st.session_state["greeted"] = True

# ---------------- Chat Logic ----------------
st.markdown("""
    <div style='text-align: center; padding: 30px;
                background: linear-gradient(90deg, #fff8e7, #f9f3e9);
                border-radius: 15px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>
        <h1 class='main-title'> The Word Companion ✝️</h1>
        <p class='subtitle'>
            An AI friend to walk with God
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h3 class='creative-prompt'>Ask, and it shall be given you — What would you like to explore?</h3>", unsafe_allow_html=True)

def is_verse_reference(text):
    return re.match(r"^[1-3]?\s?[A-Za-z]+\s\d+:\d+$", text.strip())

def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Build the conversation history from session state with correct roles
        history = []
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                history.append({'role': 'user', 'parts': [msg['content']]})
            elif msg['role'] == 'bot':
                history.append({'role': 'model', 'parts': [msg['content']]})

        if is_verse_reference(user_input):
            verse_text = fetch_verse(user_input)
            explanation = explain_verse(verse_text=verse_text, question="", history=history)
        else:
            explanation = explain_verse(verse_text="", question=user_input, history=history)

        st.session_state.messages.append({"role": "bot", "content": explanation})
        st.session_state.user_input = ""

# Display messages
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"<div class='chat-user'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    elif msg['role'] == 'bot':
        st.markdown(f"<div class='chat-bot'><strong>BibleBot:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# The main input box
st.text_input(
    "",
    placeholder="Ask your Bible Companion",
    key="user_input",
    on_change=handle_input

)
