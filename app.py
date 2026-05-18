# ================================================================
# app.py
# AI Family Relationship Chatbot — Streamlit Interface
#
# Architecture:
#   User Input → QueryHandler (NLP parsing)
#              → PrologEngine (symbolic reasoning)  [relation queries]
#              → AIMLEngine   (conversation)         [greetings/smalltalk]
#              → Streamlit UI (display)
# ================================================================

import os
import sys
import streamlit as st

# Ensure project root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.query_handler import QueryHandler
from utils.prolog_engine  import PrologEngine
from utils.aiml_engine    import AIMLEngine

# ================================================================
# PAGE CONFIG  (must be first Streamlit call)
# ================================================================
st.set_page_config(
    page_title   = "Family Relationship Chatbot",
    page_icon    = "🤖",
    layout       = "wide",
    initial_sidebar_state = "expanded",
)

# ================================================================
# CUSTOM CSS  — Modern dark-themed chatbot UI
# ================================================================
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- Root Variables ---- */
:root {
    --bg-main       : #0d0f14;
    --bg-sidebar    : #111318;
    --bg-card       : #171b24;
    --bg-input      : #1e2330;
    --border        : #2a2f3e;
    --accent        : #6c63ff;
    --accent-light  : #8b84ff;
    --accent-glow   : rgba(108,99,255,0.25);
    --green         : #22d3a0;
    --yellow        : #f5c842;
    --red           : #ff6b6b;
    --text-primary  : #e8eaf0;
    --text-secondary: #8b92a9;
    --text-muted    : #555e75;
    --user-bubble   : linear-gradient(135deg, #6c63ff, #8b84ff);
    --bot-bubble    : #1e2330;
    --radius        : 16px;
    --radius-sm     : 10px;
}

/* ---- Global Reset ---- */
* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
}

/* ---- Hide Streamlit Chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: var(--bg-main); }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ---- Sidebar Scrollbar ---- */
[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: var(--accent); border-radius: 4px;
}

/* ---- Main layout ---- */
.main-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0;
}

/* ---- Top Header Bar ---- */
.top-header {
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    padding: 14px 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.top-header .bot-avatar {
    width: 44px; height: 44px;
    background: var(--user-bubble);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 18px var(--accent-glow);
    flex-shrink: 0;
}
.top-header .bot-info h2 {
    font-family: 'Syne', sans-serif;
    font-size: 18px; font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}
.top-header .bot-info p {
    font-size: 12px; color: var(--green);
    margin: 0;
}
.status-dot {
    width: 8px; height: 8px;
    background: var(--green);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; } 50% { opacity:0.4; }
}

/* ---- Chat Container ---- */
.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: calc(100vh - 160px);
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-thumb {
    background: var(--border); border-radius: 4px;
}

/* ---- Chat Bubbles ---- */
.message-row {
    display: flex;
    gap: 10px;
    max-width: 78%;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { opacity:0; transform: translateY(10px); }
    to   { opacity:1; transform: translateY(0); }
}
.message-row.user-row {
    align-self: flex-end;
    flex-direction: row-reverse;
}
.message-row.bot-row  { align-self: flex-start; }

.avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 4px;
}
.avatar.user-avatar { background: var(--user-bubble); box-shadow: 0 0 10px var(--accent-glow); }
.avatar.bot-avatar  { background: var(--bg-card); border: 1px solid var(--border); }

.bubble {
    padding: 12px 16px;
    border-radius: var(--radius);
    line-height: 1.6;
    font-size: 14px;
    max-width: 100%;
    word-wrap: break-word;
}
.bubble.user-bubble {
    background: var(--user-bubble);
    color: #fff;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 15px var(--accent-glow);
}
.bubble.bot-bubble {
    background: var(--bot-bubble);
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

.timestamp {
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 4px;
    text-align: right;
}
.user-row .timestamp { text-align: right; }
.bot-row  .timestamp { text-align: left; }

.msg-wrap { display: flex; flex-direction: column; }

/* ---- Welcome card (shows when chat is empty) ---- */
.welcome-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    max-width: 560px;
    margin: 40px auto;
}
.welcome-card .icon {
    font-size: 56px;
    margin-bottom: 16px;
    display: block;
}
.welcome-card h1 {
    font-family: 'Syne', sans-serif;
    font-size: 26px; font-weight: 800;
    background: linear-gradient(135deg, #6c63ff, #22d3a0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 10px;
}
.welcome-card p {
    color: var(--text-secondary);
    font-size: 14px;
    margin: 0 0 20px;
}
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 16px;
}
.chip {
    background: var(--bg-input);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    border-color: var(--accent);
    color: var(--accent-light);
    background: rgba(108,99,255,0.1);
}

/* ---- Input Area ---- */
.input-area {
    background: var(--bg-card);
    border-top: 1px solid var(--border);
    padding: 14px 20px;
    position: sticky;
    bottom: 0;
}

/* Override Streamlit input styling */
.stTextInput input {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 30px !important;
    color: var(--text-primary) !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextInput input::placeholder { color: var(--text-muted) !important; }

/* Streamlit button styling */
.stButton > button {
    background: var(--user-bubble) !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 12px var(--accent-glow) !important;
    cursor: pointer !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px var(--accent-glow) !important;
}

/* Clear button */
.clear-btn > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    box-shadow: none !important;
}
.clear-btn > button:hover {
    border-color: var(--red) !important;
    color: var(--red) !important;
    box-shadow: none !important;
}

/* ---- Sidebar Components ---- */
.sidebar-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    margin-bottom: 14px;
}
.sidebar-section h3 {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-light);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 12px;
}
.relation-badge {
    display: inline-block;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.3);
    color: var(--accent-light);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    margin: 3px;
}
.member-tag {
    display: inline-block;
    background: rgba(34,211,160,0.1);
    border: 1px solid rgba(34,211,160,0.25);
    color: var(--green);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    margin: 3px;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
}
.stat-row:last-child { border-bottom: none; }
.stat-label { font-size: 12px; color: var(--text-secondary); }
.stat-value { font-size: 13px; font-weight: 600; color: var(--accent-light); }

.example-query {
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-size: 12px;
    color: var(--text-secondary);
    margin: 4px 0;
    cursor: default;
    font-family: monospace;
}
.example-query:hover {
    border-color: var(--accent);
    color: var(--text-primary);
}

/* ---- Streamlit expander ---- */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

/* ---- Divider ---- */
hr { border-color: var(--border) !important; }

/* ---- Success / Error / Info boxes ---- */
.stSuccess { background: rgba(34,211,160,0.1) !important; border-color: var(--green) !important; }
.stError   { background: rgba(255,107,107,0.1) !important; border-color: var(--red) !important; }
.stInfo    { background: rgba(108,99,255,0.1) !important; border-color: var(--accent) !important; }

/* ---- Metric ---- */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px;
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 11px; }
[data-testid="stMetricValue"] { color: var(--accent-light) !important; font-size: 20px; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# ENGINE INITIALIZATION  (cached — loads once per session)
# ================================================================

@st.cache_resource(show_spinner=False)
def load_engines():
    """
    Load all three engines once and cache them for the session.
    Returns (QueryHandler, PrologEngine, AIMLEngine, errors_dict).
    """
    base_dir   = os.path.dirname(os.path.abspath(__file__))
    pl_path    = os.path.join(base_dir, "family.pl")
    aiml_dir   = os.path.join(base_dir, "aiml_files")

    qh  = QueryHandler()
    pe  = PrologEngine(pl_path)
    ae  = AIMLEngine(aiml_dir)

    errors = {}
    if not pe.is_loaded:
        errors["prolog"] = pe.error
    if not ae.is_loaded:
        errors["aiml"]   = ae.error

    return qh, pe, ae, errors


# ================================================================
# SESSION STATE
# ================================================================

def init_session():
    """Initialize all session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "msg_count" not in st.session_state:
        st.session_state.msg_count = 0
    if "prolog_queries" not in st.session_state:
        st.session_state.prolog_queries = 0
    if "aiml_replies" not in st.session_state:
        st.session_state.aiml_replies = 0


init_session()
query_handler, prolog_engine, aiml_engine, load_errors = load_engines()


# ================================================================
# CORE CHATBOT LOGIC
# ================================================================

def get_response(user_input: str) -> tuple:
    """
    Process user input through the pipeline and return (response, source).

    Pipeline:
      1. Parse with QueryHandler
      2. If relation query → Prolog
      3. Otherwise → AIML
      4. Fallback if neither answers

    Returns:
        (response_text: str, source: str)
        source is one of: "prolog", "aiml", "fallback"
    """
    if not user_input.strip():
        return "Please type something! 😊", "fallback"

    # ---- Step 1: Parse the query ----
    parsed = query_handler.parse(user_input)

    # ---- Step 2: Prolog path (relation query detected) ----
    if parsed["is_relation_query"]:
        if parsed["error"]:
            return parsed["error"], "error"

        if not prolog_engine.is_loaded:
            return (
                "⚠️ Prolog engine is not available. Please ensure SWI-Prolog is installed.\n\n"
                f"Error: {prolog_engine.error}",
                "error"
            )

        results = prolog_engine.query(parsed["prolog_query"])
        answer  = query_handler.format_answer(
            parsed["relation"], parsed["person"], results
        )
        return answer, "prolog"

    # ---- Step 3: AIML path (conversational) ----
    if aiml_engine.is_loaded:
        aiml_response = aiml_engine.respond(user_input)
        if aiml_response:
            return aiml_response, "aiml"

    # ---- Step 4: Fallback ----
    fallback = (
        "🤔 I'm not sure how to answer that.\n\n"
        "I'm best at answering **family relationship questions**. Try:\n"
        "- `father of ali`\n"
        "- `who is grandfather of zain`\n"
        "- `chacha of laiba`\n\n"
        "Type **help** for more examples!"
    )
    return fallback, "aiml"


# ================================================================
# SIDEBAR
# ================================================================

with st.sidebar:
    # ---- Branding ----
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
        <div style="font-size:48px; margin-bottom:8px;">🤖</div>
        <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:800;
                    background:linear-gradient(135deg,#6c63ff,#22d3a0);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            FamilyBot
        </div>
        <div style="font-size:11px; color:#8b92a9; margin-top:4px;">
            Powered by Prolog + AIML + Python
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---- Engine Status ----
    st.markdown("""
    <div class="sidebar-section">
        <h3>⚙️ Engine Status</h3>
    """, unsafe_allow_html=True)

    prolog_ok = prolog_engine.is_loaded
    aiml_ok   = aiml_engine.is_loaded

    if prolog_ok:
        st.success("🧠 Prolog Engine — Online")
    else:
        st.error(f"🧠 Prolog — Offline\n{prolog_engine.error}")

    if aiml_ok:
        st.success("💬 AIML Engine — Online")
    else:
        st.warning(f"💬 AIML — Offline\n{aiml_engine.error}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Session Stats ----
    st.markdown("""
    <div class="sidebar-section">
        <h3>📊 Session Stats</h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Messages", st.session_state.msg_count)
    col2.metric("Prolog", st.session_state.prolog_queries)
    col3.metric("AIML", st.session_state.aiml_replies)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Family Members ----
    st.markdown("""
    <div class="sidebar-section">
        <h3>👥 Family Members</h3>
        <p style="font-size:11px;color:#8b92a9;margin:0 0 8px;">Males</p>
    """, unsafe_allow_html=True)

    males   = ["Ali", "Asad", "Shakeel", "Zain", "Usman", "Hamza"]
    females = ["Alia", "Shakeela", "Zaini", "Laiba", "Sana", "Nadia"]

    male_tags = "".join(f'<span class="member-tag">👨 {m}</span>' for m in males)
    st.markdown(f'<div>{male_tags}</div>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;color:#8b92a9;margin:8px 0;">Females</p>', unsafe_allow_html=True)
    female_tags = "".join(f'<span class="member-tag">👩 {f}</span>' for f in females)
    st.markdown(f'<div>{female_tags}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Supported Relations ----
    st.markdown("""
    <div class="sidebar-section">
        <h3>🔗 Supported Relations</h3>
    """, unsafe_allow_html=True)

    relations = [
        "father", "mother", "son", "daughter",
        "brother", "sister", "uncle", "aunt",
        "cousin", "nephew", "niece",
        "grandfather", "grandmother",
        "chacha", "phoophi", "maamu", "khala",
        "dada", "dadi", "nana", "nani",
        "ancestor", "descendant",
        "father-in-law", "mother-in-law",
    ]
    badges = "".join(f'<span class="relation-badge">{r}</span>' for r in relations)
    st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Example Queries ----
    with st.expander("💡 Example Queries", expanded=False):
        examples = [
            "who is father of ali",
            "father of ali",
            "can you tell me who grandfather of zain is",
            "please tell me mother of laiba",
            "chacha of laiba",
            "dada of zain",
            "what is the sister of ali",
            "who is cousin of zain",
            "ancestor of laiba",
        ]
        for ex in examples:
            st.markdown(f'<div class="example-query">▸ {ex}</div>', unsafe_allow_html=True)

    # ---- Clear Chat ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.msg_count     = 0
        st.session_state.prolog_queries = 0
        st.session_state.aiml_replies   = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Footer ----
    st.markdown("""
    <div style="text-align:center; padding:16px 0; font-size:10px; color:#555e75; border-top:1px solid #2a2f3e; margin-top:12px;">
        AI Assignment — Spring 2026<br>
        UMT · AI 473 · Family Chatbot<br>
        Prolog + AIML + Python + Streamlit
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# MAIN AREA — Header Bar
# ================================================================

st.markdown("""
<div class="top-header">
    <div class="bot-avatar">🤖</div>
    <div class="bot-info">
        <h2>Family Relationship Chatbot</h2>
        <p><span class="status-dot"></span>Online — Prolog AI Active</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ================================================================
# CHAT DISPLAY AREA
# ================================================================

chat_placeholder = st.container()

with chat_placeholder:
    if not st.session_state.messages:
        # ---- Welcome card (empty state) ----
        st.markdown("""
        <div class="welcome-card">
            <span class="icon">🏡</span>
            <h1>Family Relationship Chatbot</h1>
            <p>
                Ask me anything about the family tree!<br>
                I use <strong>Prolog symbolic reasoning</strong> to answer
                relationship queries intelligently.
            </p>
            <p style="font-size:12px; color:#555e75;">Try one of these examples:</p>
            <div class="chip-row">
                <div class="chip">father of ali</div>
                <div class="chip">grandfather of zain</div>
                <div class="chip">chacha of laiba</div>
                <div class="chip">dadi of zain</div>
                <div class="chip">hello</div>
                <div class="chip">help</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ---- Render all messages ----
        for msg in st.session_state.messages:
            role      = msg["role"]
            text      = msg["content"]
            timestamp = msg.get("time", "")
            source    = msg.get("source", "")

            if role == "user":
                st.markdown(f"""
                <div class="message-row user-row">
                    <div class="avatar user-avatar">👤</div>
                    <div class="msg-wrap">
                        <div class="bubble user-bubble">{text}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                # Source badge
                if source == "prolog":
                    badge = '<span style="font-size:10px;color:#6c63ff;margin-left:4px;">🧠 Prolog</span>'
                elif source == "aiml":
                    badge = '<span style="font-size:10px;color:#22d3a0;margin-left:4px;">💬 AIML</span>'
                else:
                    badge = ""

                # Convert markdown-like **bold** for display
                display = text.replace("**", "<strong>", 1)
                # Alternate opening/closing tags
                while "**" in display:
                    display = display.replace("**", "</strong>", 1) if display.count("**") % 2 == 0 else display.replace("**", "<strong>", 1)
                # Simpler approach: just use the text as-is (markdown renders in st.write)

                st.markdown(f"""
                <div class="message-row bot-row">
                    <div class="avatar bot-avatar">🤖</div>
                    <div class="msg-wrap">
                        <div class="bubble bot-bubble">{text}{badge}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ================================================================
# INPUT AREA
# ================================================================

st.markdown("<div class='input-area'>", unsafe_allow_html=True)

col_input, col_send = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        label       = "chat_input",
        placeholder = "Ask about a family relation... e.g. 'father of ali'",
        label_visibility = "collapsed",
        key         = "chat_input_box",
    )

with col_send:
    send_clicked = st.button("Send ➤", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# PROCESS INPUT
# ================================================================

def add_message(role, content, source=""):
    """Append a message to session history with a timestamp."""
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role"   : role,
        "content": content,
        "time"   : ts,
        "source" : source,
    })


if send_clicked and user_input.strip():
    # Add user message
    add_message("user", user_input.strip())
    st.session_state.msg_count += 1

    # Get bot response
    with st.spinner("Thinking..."):
        response, source = get_response(user_input.strip())

    # Update stats
    if source == "prolog":
        st.session_state.prolog_queries += 1
    elif source == "aiml":
        st.session_state.aiml_replies += 1

    # Add bot response
    add_message("assistant", response, source=source)

    # Rerun to refresh display
    st.rerun()

# ================================================================
# KEYBOARD SHORTCUT HINT
# ================================================================

st.markdown("""
<div style="text-align:center; padding: 6px 0; font-size:11px; color:#555e75;">
    Press <kbd style="background:#1e2330;border:1px solid #2a2f3e;
    border-radius:4px;padding:1px 6px;font-size:10px;">Enter</kbd>
    then click Send, or just click Send ➤
</div>
""", unsafe_allow_html=True)
