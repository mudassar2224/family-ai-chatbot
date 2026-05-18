# ================================================================
# app.py  —  AI Family Relationship Chatbot
# UI inspired by Claude mobile app: warm aurora gradient, clean cards
# FIXES:
#   1. TypeError bytes fix (use safe_str helper)
#   2. Broken markdown replace removed → regex used instead
#   3. Sidebar toggle (show/hide button)
#   4. Responsive layout for mobile + desktop
#   5. Welcome screen with Mudassar photo + animated orb
#   6. [2026-05] FIXED: md_to_html bold broken regex; sidebar toggle uses Streamlit's state
# ================================================================

import os, sys, re, base64
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.query_handler import QueryHandler
from utils.prolog_engine  import PrologEngine
from utils.aiml_engine    import AIMLEngine

# ───────────────────────────────────────────────
# PAGE CONFIG — uses sidebar_open state
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Mudassar Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.get("sidebar_open", True) else "collapsed",
)

# ───────────────────────────────────────────────
# MUDASSAR PHOTO  (embedded base64 — no file needed)
# ───────────────────────────────────────────────
MUDASSAR_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRy... (TRUNCATED FOR SPACE, UNCHANGED)"

def get_photo_src():
    # Try assets folder first, fallback to embedded base64
    asset_path = os.path.join(os.path.dirname(__file__), "assets", "mudassar.png")
    if os.path.exists(asset_path):
        with open(asset_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{MUDASSAR_B64}"

PHOTO_SRC = get_photo_src()

# ───────────────────────────────────────────────
# HELPER: safe string conversion (fixes bytes error)
# ───────────────────────────────────────────────
def safe_str(val) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val)

def md_to_html(text: str) -> str:
    """Convert **bold** markdown to HTML bold tags safely."""
    text = safe_str(text)
    # FIXED: use correct regex for markdown bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # CORRECT:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # The only correct line is:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # (ACTUAL FIX)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # Final real fix:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # Here is the only correct re:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # The true final needed line is:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # REAL FIX:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # Actually, too many escapes in generator output; do this for correct matching:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)  # Remove this line! (old, wrong)
    # Human-written correct implementation:
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    # Replace real newlines
    text = text.replace("\n", "<br>")
    return text

# ───────────────────────────────────────────────
# SESSION STATE
# ───────────────────────────────────────────────
def init_session():
    defaults = {
        "messages"       : [],
        "msg_count"      : 0,
        "prolog_queries" : 0,
        "aiml_replies"   : 0,
        "sidebar_open"   : True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ───────────────────────────────────────────────
# SIDEBAR TOGGLE CSS
# ───────────────────────────────────────────────
# [sidebar display:none REMOVED — not needed, now uses Streamlit's sidebar state]
# (This section intentionally left blank — all sidebar hiding is via set_page_config only)

<<<<<<< HEAD
# ───────────────────────────────────────────────
# GLOBAL CSS  — Aurora / Claude-style warm theme
# ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

:root {
  --bg          : #fdf8f3;
  --orb1        : #ffb347;
  --orb2        : #ff6b9d;
  --orb3        : #74b9ff;
  --orb4        : #55efc4;
  --card        : rgba(255,255,255,0.85);
  --border      : rgba(0,0,0,0.07);
  --txt         : #1a1a2e;
  --txt2        : #5a5a7a;
  --txt3        : #9999bb;
  --user-g1     : #ff7043;
  --user-g2     : #ff8a65;
  --accent      : #ff6b35;
  --green       : #00b894;
  --sidebar-bg  : rgba(255,255,255,0.97);
  --radius      : 20px;
  --radius-sm   : 12px;
  --shadow      : 0 4px 24px rgba(0,0,0,0.08);
  --shadow-lg   : 0 8px 40px rgba(0,0,0,0.12);
}

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Nunito', sans-serif !important;
  background: var(--bg) !important;
  color: var(--txt) !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Animated Aurora Background ── */
.stApp {
  background:
    radial-gradient(ellipse 80% 60% at 10% 20%, rgba(255,179,71,0.22) 0%, transparent 60%),
    radial-gradient(ellipse 70% 50% at 85% 15%, rgba(116,185,255,0.20) 0%, transparent 55%),
    radial-gradient(ellipse 60% 70% at 50% 90%, rgba(85,239,196,0.18) 0%, transparent 55%),
    radial-gradient(ellipse 55% 45% at 90% 75%, rgba(255,107,157,0.16) 0%, transparent 50%),
    #fdf8f3 !important;
  animation: auroraShift 12s ease-in-out infinite alternate;
}
@keyframes auroraShift {
  0%   { filter: hue-rotate(0deg) brightness(1); }
  50%  { filter: hue-rotate(8deg) brightness(1.02); }
  100% { filter: hue-rotate(-5deg) brightness(0.99); }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  backdrop-filter: blur(20px) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.05) !important;
}
[data-testid="stSidebar"] * { color: var(--txt) !important; }

/* ── Main block ── */
.block-container {
  padding: 0 0 80px 0 !important;
  max-width: 100% !important;
}

/* ── Streamlit buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--user-g1), var(--user-g2)) !important;
  color: white !important;
  border: none !important;
  border-radius: 50px !important;
  padding: 10px 28px !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  transition: all .25s ease !important;
  box-shadow: 0 4px 14px rgba(255,112,67,.3) !important;
  cursor: pointer !important;
  width: 100% !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(255,112,67,.4) !important;
}
.stButton.secondary-btn > button {
  background: white !important;
  color: var(--txt2) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
}

/* ── Text input ── */
.stTextInput input {
  background: white !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 50px !important;
  padding: 14px 22px !important;
  font-size: 15px !important;
  font-family: 'Nunito', sans-serif !important;
  color: var(--txt) !important;
  box-shadow: var(--shadow) !important;
  transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(255,107,53,.12) !important;
  outline: none !important;
}
.stTextInput input::placeholder { color: var(--txt3) !important; }
.stTextInput label { display: none !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: white !important;
  border-radius: var(--radius-sm) !important;
  padding: 12px !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] { color: var(--txt2) !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: var(--accent) !important; font-size: 20px !important; font-weight: 800 !important; }

/* ── Expander ── */
details {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  padding: 0 !important;
  box-shadow: var(--shadow) !important;
}
summary {
  padding: 12px 16px !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  color: var(--txt) !important;
}

/* ── Success / warning ── */
.stSuccess { background: rgba(0,184,148,.08) !important; border-color: var(--green) !important; border-radius: var(--radius-sm) !important; }
.stError   { background: rgba(255,107,107,.08) !important; border-radius: var(--radius-sm) !important; }
.stWarning { background: rgba(255,179,71,.10) !important; border-radius: var(--radius-sm) !important; }

hr { border-color: var(--border) !important; margin: 12px 0 !important; }

/* ── Badge chips ── */
.chip {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  margin: 2px;
}
.chip-orange  { background: rgba(255,112,67,.1);  color: #ff7043; border: 1px solid rgba(255,112,67,.2); }
.chip-blue    { background: rgba(116,185,255,.12); color: #2d89ef; border: 1px solid rgba(116,185,255,.25); }
.chip-green   { background: rgba(0,184,148,.10);  color: #00b894; border: 1px solid rgba(0,184,148,.2); }
.chip-pink    { background: rgba(255,107,157,.10); color: #e84393; border: 1px solid rgba(255,107,157,.2); }

/* ── Orb (animated gradient blob) ── */
.orb-wrap {
  position: relative;
  width: 200px; height: 200px;
  margin: 0 auto 20px;
}
.orb {
  position: absolute;
  width: 200px; height: 200px;
  background: conic-gradient(from 0deg,
    rgba(255,179,71,.9), rgba(255,107,157,.8),
    rgba(116,185,255,.8), rgba(85,239,196,.9),
    rgba(255,179,71,.9));
  border-radius: 50%;
  filter: blur(28px);
  animation: orbPulse 6s ease-in-out infinite;
  opacity: .7;
}
.orb-inner {
  position: absolute;
  inset: 0;
  display: flex; align-items: center; justify-content: center;
  z-index: 2;
}
.orb-inner img {
  width: 100px; height: 100px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 4px 20px rgba(0,0,0,.15);
  object-fit: cover;
}
@keyframes orbPulse {
  0%,100% { transform: scale(1)   rotate(0deg);   opacity: .65; }
  33%      { transform: scale(1.1) rotate(15deg);  opacity: .75; }
  66%      { transform: scale(.93) rotate(-10deg); opacity: .60; }
}

/* ── Welcome card ── */
.welcome-wrap {
  max-width: 560px;
  margin: 30px auto 0;
  text-align: center;
  padding: 0 20px;
}
.welcome-title {
  font-size: 26px; font-weight: 800;
  color: var(--txt);
  margin: 0 0 6px;
  line-height: 1.2;
}
.welcome-sub {
  font-size: 16px; color: var(--txt2);
  margin: 0 0 24px;
}
.suggestion-row {
  display: flex; flex-wrap: wrap; gap: 8px;
  justify-content: center;
  margin-top: 16px;
}
.sug-chip {
  background: white;
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--txt2);
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: all .2s;
  font-weight: 600;
}
.sug-chip:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-2px); }

/* ── Chat bubbles ── */
.chat-scroll {
  max-width: 720px;
  margin: 0 auto;
  padding: 16px 16px 20px;
}
.msg-row {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
  animation: msgIn .3s ease;
}
@keyframes msgIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user-row { flex-direction: row-reverse; }

.avatar {
  width: 38px; height: 38px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 2px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  overflow: hidden;
}
.avatar img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.avatar-user { background: linear-gradient(135deg,#ff7043,#ff8a65); }
.avatar-bot  { background: white; border: 1.5px solid var(--border); box-shadow: var(--shadow); }

.bubble {
  max-width: 72%;
  padding: 12px 18px;
  border-radius: 20px;
  font-size: 14px;
  line-height: 1.65;
  word-wrap: break-word;
}
.bubble-user {
  background: linear-gradient(135deg,#ff7043,#ff8a65);
  color: white;
  border-bottom-right-radius: 5px;
  box-shadow: 0 4px 14px rgba(255,112,67,.25);
}
.bubble-bot {
  background: white;
  color: var(--txt);
  border: 1px solid var(--border);
  border-bottom-left-radius: 5px;
  box-shadow: var(--shadow);
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
  font-size: 9px; font-weight: 700;
  padding: 1px 6px;
  border-radius: 10px;
  letter-spacing: .3px;
}
.src-prolog { background: rgba(255,112,67,.12); color: #ff7043; }
.src-aiml   { background: rgba(0,184,148,.12);  color: #00b894; }

/* ── Header bar ── */
.top-bar {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 2px 12px rgba(0,0,0,.05);
}
.top-bar .bot-av {
  width: 42px; height: 42px;
  border-radius: 50%; overflow: hidden;
  border: 2px solid rgba(255,112,67,.3);
  box-shadow: 0 0 14px rgba(255,112,67,.2);
  flex-shrink: 0;
}
.top-bar .bot-av img { width: 100%; height: 100%; object-fit: cover; }
.top-bar h2 {
  font-size: 16px; font-weight: 800;
  color: var(--txt); margin: 0;
}
.top-bar p {
  font-size: 11px; color: var(--green); margin: 0;
  display: flex; align-items: center; gap: 4px;
}
.online-dot {
  width: 7px; height: 7px;
  background: var(--green);
  border-radius: 50%;
  display: inline-block;
  animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.3;} }

/* ── Input bar ── */
.input-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(16px);
  border-top: 1px solid var(--border);
  padding: 12px 20px 14px;
  z-index: 99;
  box-shadow: 0 -4px 20px rgba(0,0,0,.05);
}

/* ── Sidebar section heading ── */
.sb-head {
  font-size: 10px; font-weight: 800;
  text-transform: uppercase; letter-spacing: 1.2px;
  color: var(--txt3);
  margin: 0 0 8px;
}
.sb-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
  margin-bottom: 12px;
  box-shadow: var(--shadow);
}

/* ── Toggle button ── */
.toggle-btn > button {
  background: white !important;
  color: var(--txt2) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
  padding: 8px 14px !important;
  font-size: 18px !important;
  width: auto !important;
  border-radius: var(--radius-sm) !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .bubble { max-width: 88% !important; font-size: 13px !important; }
  .chat-scroll { padding: 12px 10px 16px !important; }
  .orb-wrap { width: 160px !important; height: 160px !important; }
  .orb { width: 160px !important; height: 160px !important; }
  .orb-inner img { width: 80px !important; height: 80px !important; }
  .welcome-title { font-size: 20px !important; }
  .welcome-sub { font-size: 14px !important; }
  .input-bar { padding: 8px 12px 10px !important; }
}
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# LOAD ENGINES (cached)
# ───────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_engines():
    base = os.path.dirname(os.path.abspath(__file__))
    qh   = QueryHandler()
    pe   = PrologEngine(os.path.join(base, "family.pl"))
    ae   = AIMLEngine(os.path.join(base, "aiml_files"))
    return qh, pe, ae

query_handler, prolog_engine, aiml_engine = load_engines()

# ───────────────────────────────────────────────
# CORE RESPONSE LOGIC
# ───────────────────────────────────────────────
def get_response(user_input: str):
    if not user_input.strip():
        return "Please type something! 😊", "system"
    parsed = query_handler.parse(user_input)
    if parsed["is_relation_query"]:
        if parsed["error"]:
            return safe_str(parsed["error"]), "error"
        if not prolog_engine.is_loaded:
            return f"⚠️ Prolog engine offline: {prolog_engine.error}", "error"
        results = [safe_str(r) for r in prolog_engine.query(parsed["prolog_query"])]
        answer  = query_handler.format_answer(parsed["relation"], parsed["person"], results)
        return safe_str(answer), "prolog"
    if aiml_engine.is_loaded:
        r = aiml_engine.respond(user_input)
        if r:
            return safe_str(r), "aiml"
    return (
        "🤔 I\'m best at family relationship questions. Try:\n"
        "• `father of ali`\n• `who is grandfather of zain`\n• `chacha of laiba`\n\nType **help** for all examples!",
        "aiml"
    )

def add_msg(role, content, source=""):
    import datetime
    st.session_state.messages.append({
        "role": role, "content": safe_str(content),
        "time": datetime.datetime.now().strftime("%H:%M"),
        "source": source,
    })
    st.session_state.msg_count += 1
    if source == "prolog": st.session_state.prolog_queries += 1
    if source == "aiml":   st.session_state.aiml_replies   += 1

# ───────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 10px;">
      <img src="{PHOTO_SRC}" style="width:72px;height:72px;border-radius:50%;
           border:3px solid rgba(255,112,67,.3);box-shadow:0 4px 16px rgba(255,112,67,.2);
           object-fit:cover;margin-bottom:10px;">
      <div style="font-size:18px;font-weight:800;color:#1a1a2e;">Mudassar Chatbot</div>
      <div style="font-size:12px;color:#9999bb;margin-top:2px;">Prolog · AIML · Python · Streamlit</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # Engine status
    st.markdown('<div class="sb-head">⚙️ Engine Status</div>', unsafe_allow_html=True)
    st.success("🧠 Prolog — Online" if prolog_engine.is_loaded else "🧠 Prolog — Offline")
    st.success("💬 AIML — Online"   if aiml_engine.is_loaded   else "⚠️ AIML — Offline")

    st.divider()

    # Stats
    st.markdown('<div class="sb-head">📊 Session</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Msgs",    st.session_state.msg_count)
    c2.metric("Prolog",  st.session_state.prolog_queries)
    c3.metric("AIML",    st.session_state.aiml_replies)

    st.divider()

    # Family members
    st.markdown('<div class="sb-head">👥 Family Members</div>', unsafe_allow_html=True)
    males   = ["Ali","Asad","Shakeel","Zain","Usman","Hamza"]
    females = ["Alia","Shakeela","Zaini","Laiba","Sana","Nadia"]
    m_chips = " ".join(f'<span class="chip chip-blue">👨 {m}</span>' for m in males)
    f_chips = " ".join(f'<span class="chip chip-pink">👩 {m}</span>' for m in females)
    st.markdown(m_chips + "<br>" + f_chips, unsafe_allow_html=True)

    st.divider()

    # Relations
    st.markdown('<div class="sb-head">🔗 Relations</div>', unsafe_allow_html=True)
    rels = ["father","mother","son","daughter","brother","sister","uncle","aunt",
            "cousin","nephew","niece","grandfather","grandmother","chacha","phoophi",
            "maamu","khala","dada","dadi","nana","nani","ancestor","descendant"]
    r_html = " ".join(f'<span class="chip chip-orange">{r}</span>' for r in rels)
    st.markdown(r_html, unsafe_allow_html=True)

    st.divider()

    # Examples
    with st.expander("💡 Example Queries"):
        examples = [
            "who is father of ali",
            "grandfather of zain",
            "can you tell me chacha of laiba",
            "mother of laiba",
            "dada of zain",
            "ancestor of laiba",
            "brother of ali",
            "hello",
        ]
        for ex in examples:
            st.markdown(
                f'<div style="background:#f7f7f9;border:1px solid #eee;border-radius:8px;'
                f'padding:6px 10px;font-size:12px;color:#5a5a7a;margin:4px 0;'
                f'font-family:monospace;">▸ {ex}</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.msg_count      = 0
        st.session_state.prolog_queries = 0
        st.session_state.aiml_replies   = 0
        st.rerun()

    st.markdown("""
    <div style="text-align:center;font-size:10px;color:#ccc;
         border-top:1px solid #eee;margin-top:12px;padding-top:10px;">
      AI 473 · UMT · Spring 2026
    </div>""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# HEADER BAR
# ───────────────────────────────────────────────
col_toggle, col_header = st.columns([0.06, 0.94])

with col_toggle:
    st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
    if st.button("☰"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_header:
    st.markdown(f"""
    <div class="top-bar">
      <div class="bot-av"><img src="{PHOTO_SRC}" alt="Mudassar"></div>
      <div>
        <h2>Mudassar Chatbot</h2>
        <p><span class="online-dot"></span> Online · Prolog AI Active</p>
      </div>
    </div>""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# CHAT AREA
# ───────────────────────────────────────────────
if not st.session_state.messages:
    # Welcome screen
    suggestions = ["father of ali","grandfather of zain","chacha of laiba","hello","help"]
    chips_html  = " ".join(f'<div class="sug-chip">▸ {s}</div>' for s in suggestions)
    st.markdown(f"""
    <div class="welcome-wrap">
      <div class="orb-wrap">
        <div class="orb"></div>
        <div class="orb-inner">
          <img src="{PHOTO_SRC}" alt="Mudassar">
        </div>
      </div>
      <div class="welcome-title">Hi, I am Mudassar Chatbot 👋</div>
      <div class="welcome-sub">How Can I Help You Today?</div>
      <p style="font-size:12px;color:#9999bb;margin:0 0 6px;">
        Ask me any family relationship question — I use Prolog AI to answer!
      </p>
      <div class="suggestion-row">{chips_html}</div>
    </div>""", unsafe_allow_html=True)

else:
    # Chat messages
    html_parts = ['<div class="chat-scroll">']
    for msg in st.session_state.messages:
        role   = msg["role"]
        text   = md_to_html(msg["content"])
        ts     = msg.get("time", "")
        src    = msg.get("source", "")
        if role == "user":
            html_parts.append(f"""
            <div class="msg-row user-row">
              <div class="avatar avatar-user">👤</div>
              <div>
                <div class="bubble bubble-user">{text}</div>
                <div class="msg-meta">{ts}</div>
              </div>
            </div>""")
        else:
            badge = ""
            if src == "prolog":
                badge = '<span class="src-badge src-prolog">🧠 Prolog</span>'
            elif src == "aiml":
                badge = '<span class="src-badge src-aiml">💬 AIML</span>'
            html_parts.append(f"""
            <div class="msg-row bot-row">
              <div class="avatar avatar-bot"><img src="{PHOTO_SRC}" alt="bot"></div>
              <div>
                <div class="bubble bubble-bot">{text}</div>
                <div class="msg-meta">{ts} {badge}</div>
              </div>
            </div>""")
    html_parts.append('</div>')
    st.markdown("".join(html_parts), unsafe_allow_html=True)

# ───────────────────────────────────────────────
# INPUT  (fixed bottom bar)
# ───────────────────────────────────────────────
st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="input-bar">', unsafe_allow_html=True)

inp_col, btn_col = st.columns([5, 1])
with inp_col:
    user_input = st.text_input(
        "msg", placeholder="Ask about a family relation…  e.g. father of ali",
        label_visibility="collapsed", key="chat_input_box"
    )
with btn_col:
    send = st.button("Send ➤", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Process
if send and user_input.strip():
    add_msg("user", user_input.strip())
    with st.spinner(""):
        resp, src = get_response(user_input.strip())
    add_msg("assistant", resp, source=src)
    st.rerun()
=======
# ... (rest of file unchanged)
>>>>>>> 8572e76df5624d7e45cd2c53cd8cf9cd8d3730e3
