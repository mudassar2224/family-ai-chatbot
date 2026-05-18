# ================================================================
# app.py  —  AI Family Relationship Chatbot
# UI inspired by Claude mobile app: warm aurora gradient, clean cards
# FIXED: Chat HTML structure, avatar images, and all bugs
# ================================================================

import os
import sys
import re
import base64
import datetime
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.query_handler import QueryHandler
from utils.prolog_engine import PrologEngine
from utils.aiml_engine import AIMLEngine

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Mudassar Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# CONSTANTS - Shortened base64 for brevity (use your full one)
# ================================================================
MUDASSAR_B64 = "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\\\\\\\\\\\\\\'"

PHOTO_SRC = f"data:image/png;base64,{MUDASSAR_B64}"

# ================================================================
# HELPER FUNCTIONS
# ================================================================
def safe_str(val) -> str:
    """Safe string conversion - fixes bytes error"""
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val)


def md_to_html(text: str) -> str:
    """Convert **bold** markdown to HTML bold tags safely."""
    text = safe_str(text)
    # Match **text** pattern correctly
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = text.replace("\n", "<br>")
    return text


def get_photo_src() -> str:
    """Get photo source from assets or embedded base64"""
    asset_path = os.path.join(os.path.dirname(__file__), "assets", "mudassar.png")
    if os.path.exists(asset_path):
        with open(asset_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return PHOTO_SRC


def init_session():
    """Initialize session state with defaults"""
    defaults = {
        "messages": [],
        "msg_count": 0,
        "prolog_queries": 0,
        "aiml_replies": 0,
        "sidebar_open": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_message(role: str, content: str, source: str = ""):
    """Add a message to chat history"""
    st.session_state.messages.append({
        "role": role,
        "content": safe_str(content),
        "time": datetime.datetime.now().strftime("%H:%M"),
        "source": source,
    })
    st.session_state.msg_count += 1
    if source == "prolog":
        st.session_state.prolog_queries += 1
    elif source == "aiml":
        st.session_state.aiml_replies += 1


# ================================================================
# LOAD ENGINES (cached)
# ================================================================
@st.cache_resource(show_spinner=False)
def load_engines():
    """Load and cache all AI engines"""
    base = os.path.dirname(os.path.abspath(__file__))
    qh = QueryHandler()
    pe = PrologEngine(os.path.join(base, "family.pl"))
    ae = AIMLEngine(os.path.join(base, "aiml_files"))
    return qh, pe, ae


# ================================================================
# INITIALIZE
# ================================================================
init_session()
query_handler, prolog_engine, aiml_engine = load_engines()
FINAL_PHOTO_SRC = get_photo_src()

# ================================================================
# SIDEBAR TOGGLE FUNCTION
# ================================================================
def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open


# ================================================================
# APPLY SIDEBAR CSS BASED ON STATE
# ================================================================
if not st.session_state.sidebar_open:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ================================================================
# CORE RESPONSE LOGIC
# ================================================================
def get_response(user_input: str):
    """Generate bot response based on user input"""
    if not user_input.strip():
        return "Please type something! 😊", "system"

    parsed = query_handler.parse(user_input)

    if parsed["is_relation_query"]:
        if parsed["error"]:
            return safe_str(parsed["error"]), "error"
        if not prolog_engine.is_loaded:
            return f"⚠️ Prolog engine offline: {prolog_engine.error}", "error"

        results = [safe_str(r) for r in prolog_engine.query(parsed["prolog_query"])]
        answer = query_handler.format_answer(parsed["relation"], parsed["person"], results)
        return safe_str(answer), "prolog"

    if aiml_engine.is_loaded:
        response = aiml_engine.respond(user_input)
        if response:
            return safe_str(response), "aiml"

    return (
        "🤔 I'm best at family relationship questions. Try:\n"
        "• `father of ali`\n• `who is grandfather of zain`\n• `chacha of laiba`\n\n"
        "Type **help** for all examples!",
        "aiml"
    )


# ================================================================
# GLOBAL CSS
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #fdf8f3;
    --orb1: #ffb347;
    --orb2: #ff6b9d;
    --orb3: #74b9ff;
    --orb4: #55efc4;
    --card: rgba(255,255,255,0.85);
    --border: rgba(0,0,0,0.07);
    --txt: #1a1a2e;
    --txt2: #5a5a7a;
    --txt3: #9999bb;
    --user-g1: #ff7043;
    --user-g2: #ff8a65;
    --accent: #ff6b35;
    --green: #00b894;
    --sidebar-bg: rgba(255,255,255,0.97);
    --radius: 20px;
    --radius-sm: 12px;
    --shadow: 0 4px 24px rgba(0,0,0,0.08);
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background: var(--bg) !important;
    color: var(--txt) !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* Animated Aurora Background */
.stApp {
    background: radial-gradient(ellipse 80% 60% at 10% 20%, rgba(255,179,71,0.22) 0%, transparent 60%),
                radial-gradient(ellipse 70% 50% at 85% 15%, rgba(116,185,255,0.20) 0%, transparent 55%),
                radial-gradient(ellipse 60% 70% at 50% 90%, rgba(85,239,196,0.18) 0%, transparent 55%),
                radial-gradient(ellipse 55% 45% at 90% 75%, rgba(255,107,157,0.16) 0%, transparent 50%),
                #fdf8f3 !important;
    animation: auroraShift 12s ease-in-out infinite alternate;
}

@keyframes auroraShift {
    0% { filter: hue-rotate(0deg) brightness(1); }
    50% { filter: hue-rotate(8deg) brightness(1.02); }
    100% { filter: hue-rotate(-5deg) brightness(0.99); }
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 4px; }

[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.05) !important;
}

.block-container {
    padding: 0 0 80px 0 !important;
    max-width: 100% !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--user-g1), var(--user-g2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 10px 28px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

.stTextInput input {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 50px !important;
    padding: 14px 22px !important;
    font-size: 15px !important;
    box-shadow: var(--shadow) !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    outline: none !important;
}
.stTextInput label { display: none !important; }

[data-testid="stMetric"] {
    background: white !important;
    border-radius: var(--radius-sm) !important;
    padding: 12px !important;
    border: 1px solid var(--border) !important;
}

.chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
}
.chip-orange { background: rgba(255,112,67,0.1); color: #ff7043; }
.chip-blue { background: rgba(116,185,255,0.12); color: #2d89ef; }
.chip-pink { background: rgba(255,107,157,0.10); color: #e84393; }

/* Orb Animation */
.orb-wrap {
    position: relative;
    width: 200px;
    height: 200px;
    margin: 0 auto 20px;
}
.orb {
    position: absolute;
    width: 200px;
    height: 200px;
    background: conic-gradient(from 0deg, rgba(255,179,71,0.9), rgba(255,107,157,0.8), rgba(116,185,255,0.8), rgba(85,239,196,0.9));
    border-radius: 50%;
    filter: blur(28px);
    animation: orbPulse 6s ease-in-out infinite;
    opacity: 0.7;
}
.orb-inner {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
}
.orb-inner img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid white;
    object-fit: cover;
}
@keyframes orbPulse {
    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.65; }
    33% { transform: scale(1.1) rotate(15deg); opacity: 0.75; }
    66% { transform: scale(0.93) rotate(-10deg); opacity: 0.60; }
}

.welcome-wrap {
    max-width: 560px;
    margin: 30px auto 0;
    text-align: center;
    padding: 0 20px;
}
.welcome-title {
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 6px;
}
.welcome-sub {
    font-size: 16px;
    color: var(--txt2);
    margin: 0 0 24px;
}
.suggestion-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 16px;
}
.sug-chip {
    background: white;
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}
.sug-chip:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-2px); }

/* Chat Bubbles - FIXED STRUCTURE */
.chat-scroll {
    max-width: 720px;
    margin: 0 auto;
    padding: 16px 16px 20px;
}
.msg-row {
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
    animation: msgIn 0.3s ease;
}
@keyframes msgIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.msg-row.user-row { flex-direction: row-reverse; }

.avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    overflow: hidden;
}
.avatar img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.avatar-user { background: linear-gradient(135deg, #ff7043, #ff8a65); }
.avatar-bot { background: white; border: 1.5px solid var(--border); }

.bubble {
    max-width: 72%;
    padding: 12px 18px;
    border-radius: 20px;
    font-size: 14px;
    line-height: 1.65;
    word-wrap: break-word;
}
.bubble-user {
    background: linear-gradient(135deg, #ff7043, #ff8a65);
    color: white;
    border-bottom-right-radius: 5px;
}
.bubble-bot {
    background: white;
    color: var(--txt);
    border: 1px solid var(--border);
    border-bottom-left-radius: 5px;
}
.msg-meta {
    font-size: 10px;
    color: var(--txt3);
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.user-row .msg-meta { justify-content: flex-end; }
.src-badge {
    font-size: 9px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 10px;
}
.src-prolog { background: rgba(255,112,67,0.12); color: #ff7043; }
.src-aiml { background: rgba(0,184,148,0.12); color: #00b894; }

.top-bar {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.top-bar .bot-av {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}
.top-bar .bot-av img { width: 100%; height: 100%; object-fit: cover; }
.top-bar h2 { font-size: 16px; font-weight: 800; margin: 0; }
.top-bar p { font-size: 11px; color: var(--green); margin: 0; display: flex; align-items: center; gap: 4px; }
.online-dot {
    width: 7px;
    height: 7px;
    background: var(--green);
    border-radius: 50%;
    display: inline-block;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(16px);
    border-top: 1px solid var(--border);
    padding: 12px 20px 14px;
    z-index: 99;
}

.sb-head {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--txt3);
    margin: 0 0 8px;
}

.toggle-btn > button {
    background: white !important;
    color: var(--txt2) !important;
    border: 1px solid var(--border) !important;
    padding: 8px 14px !important;
    font-size: 18px !important;
    width: auto !important;
}

@media (max-width: 768px) {
    .bubble { max-width: 88% !important; font-size: 13px !important; }
    .orb-wrap { width: 160px !important; height: 160px !important; }
    .orb { width: 160px !important; height: 160px !important; }
    .orb-inner img { width: 80px !important; height: 80px !important; }
    .welcome-title { font-size: 20px !important; }
}
</style>
""", unsafe_allow_html=True)


# ================================================================
# SIDEBAR CONTENT
# ================================================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 10px;">
        <img src="{FINAL_PHOTO_SRC}" style="width:72px;height:72px;border-radius:50%;
             border:3px solid rgba(255,112,67,.3);object-fit:cover;margin-bottom:10px;">
        <div style="font-size:18px;font-weight:800;">Mudassar Chatbot</div>
        <div style="font-size:12px;color:#9999bb;">Prolog · AIML · Python · Streamlit</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sb-head">⚙️ Engine Status</div>', unsafe_allow_html=True)
    st.success("🧠 Prolog — Online" if prolog_engine.is_loaded else "🧠 Prolog — Offline")
    st.success("💬 AIML — Online" if aiml_engine.is_loaded else "⚠️ AIML — Offline")

    st.divider()

    st.markdown('<div class="sb-head">📊 Session</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Msgs", st.session_state.msg_count)
    c2.metric("Prolog", st.session_state.prolog_queries)
    c3.metric("AIML", st.session_state.aiml_replies)

    st.divider()

    st.markdown('<div class="sb-head">👥 Family Members</div>', unsafe_allow_html=True)
    males = ["Ali", "Asad", "Shakeel", "Zain", "Usman", "Hamza"]
    females = ["Alia", "Shakeela", "Zaini", "Laiba", "Sana", "Nadia"]
    male_chips = " ".join(f'<span class="chip chip-blue">👨 {m}</span>' for m in males)
    female_chips = " ".join(f'<span class="chip chip-pink">👩 {f}</span>' for f in females)
    st.markdown(male_chips + "<br>" + female_chips, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sb-head">🔗 Relations</div>', unsafe_allow_html=True)
    relations = ["father", "mother", "son", "daughter", "brother", "sister", "uncle", "aunt",
                 "cousin", "nephew", "niece", "grandfather", "grandmother", "chacha", "phoophi",
                 "maamu", "khala", "dada", "dadi", "nana", "nani", "ancestor", "descendant"]
    rel_html = " ".join(f'<span class="chip chip-orange">{r}</span>' for r in relations)
    st.markdown(rel_html, unsafe_allow_html=True)

    st.divider()

    with st.expander("💡 Example Queries"):
        examples = ["who is father of ali", "grandfather of zain", "chacha of laiba", "mother of laiba", "hello"]
        for ex in examples:
            st.markdown(f'<div style="background:#f7f7f9;border:1px solid #eee;border-radius:8px;padding:6px 10px;font-size:12px;margin:4px 0;">▸ {ex}</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.prolog_queries = 0
        st.session_state.aiml_replies = 0
        st.rerun()

    st.markdown('<div style="text-align:center;font-size:10px;color:#ccc;border-top:1px solid #eee;margin-top:12px;padding-top:10px;">AI 473 · UMT · Spring 2026</div>', unsafe_allow_html=True)


# ================================================================
# HEADER BAR WITH TOGGLE BUTTON
# ================================================================
col_toggle, col_header = st.columns([0.06, 0.94])

with col_toggle:
    st.button("☰", key="toggle_btn", on_click=toggle_sidebar, use_container_width=True)

with col_header:
    st.markdown(f"""
    <div class="top-bar" style="background:transparent; padding:0;">
        <div class="bot-av"><img src="{FINAL_PHOTO_SRC}" alt="Mudassar"></div>
        <div>
            <h2>Mudassar Chatbot</h2>
            <p><span class="online-dot"></span> Online · Prolog AI Active</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# CHAT AREA
# ================================================================
if not st.session_state.messages:
    # Welcome Screen
    suggestions = ["father of ali", "grandfather of zain", "chacha of laiba", "hello", "help"]
    chips_html = "".join(f'<div class="sug-chip" onclick="this.click()">▸ {s}</div>' for s in suggestions)

    st.markdown(f"""
    <div class="welcome-wrap">
        <div class="orb-wrap">
            <div class="orb"></div>
            <div class="orb-inner">
                <img src="{FINAL_PHOTO_SRC}" alt="Mudassar">
            </div>
        </div>
        <div class="welcome-title">Hi, I am Mudassar Chatbot 👋</div>
        <div class="welcome-sub">How Can I Help You Today?</div>
        <p style="font-size:12px;color:#9999bb;">Ask me any family relationship question — I use Prolog AI to answer!</p>
        <div class="suggestion-row">{chips_html}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Chat Messages Display - FIXED HTML STRUCTURE
    for msg in st.session_state.messages:
        role = msg["role"]
        text = md_to_html(msg["content"])
        timestamp = msg.get("time", "")
        source = msg.get("source", "")

        if role == "user":
            # User message
            st.markdown(f"""
            <div class="msg-row user-row">
                <div class="avatar avatar-user">👤</div>
                <div style="flex:1">
                    <div class="bubble bubble-user">{text}</div>
                    <div class="msg-meta">{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Bot message
            badge = ""
            if source == "prolog":
                badge = '<span class="src-badge src-prolog">🧠 Prolog</span>'
            elif source == "aiml":
                badge = '<span class="src-badge src-aiml">💬 AIML</span>'

            st.markdown(f"""
            <div class="msg-row bot-row">
                <div class="avatar avatar-bot">
                    <img src="{FINAL_PHOTO_SRC}" alt="bot" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">
                </div>
                <div style="flex:1">
                    <div class="bubble bubble-bot">{text}</div>
                    <div class="msg-meta">{timestamp} {badge}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ================================================================
# INPUT BAR (Fixed at bottom)
# ================================================================
st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="input-bar">', unsafe_allow_html=True)

input_col, button_col = st.columns([5, 1])

with input_col:
    user_input = st.text_input(
        "message",
        placeholder="Ask about a family relation… e.g. father of ali",
        label_visibility="collapsed",
        key="chat_input"
    )

with button_col:
    send_button = st.button("Send ➤", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# PROCESS USER INPUT
# ================================================================
if send_button and user_input and user_input.strip():
    clean_input = user_input.strip()

    # Add user message
    add_message("user", clean_input)

    # Get bot response
    bot_response, source_used = get_response(clean_input)

    # Add bot response
    add_message("assistant", bot_response, source=source_used)

    # Rerun to refresh UI
    st.rerun()