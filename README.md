# 🤖 AI Family Relationship Chatbot

> **AI 473 — Artificial Neural Networks & Deep Learning**  
> **Assignment 1** | University of Management and Technology (UMT) | Spring 2026

---

## 📌 Overview

An intelligent family relationship chatbot that combines:

| Layer | Technology | Role |
|-------|-----------|------|
| 🧠 Reasoning | **Prolog (SWI-Prolog + pyswip)** | Symbolic AI, 36 rules, family KB |
| 💬 Conversation | **AIML (python-aiml)** | Greetings, small talk, help |
| 🐍 Middleware | **Python** | NLP parsing, integration logic |
| 🌐 Interface | **Streamlit** | Modern web-based chat UI |

The chatbot can answer **any natural language variation** of family relationship questions:

```
"who is father of ali"          ✅
"father of ali"                  ✅
"can you tell me who grandfather of zain is"   ✅
"please tell me the chacha of laiba"            ✅
"what is dada of zain"          ✅
```

---

## 🗂️ Project Structure

```
family_chatbot/
│
├── app.py                    # Streamlit web application (main entry)
├── family.pl                 # Prolog knowledge base (5 fact types, 36 rules)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── aiml_files/
│   └── family_chatbot.aiml   # AIML patterns (greetings, small talk, help)
│
├── utils/
│   ├── __init__.py           # Package exports
│   ├── query_handler.py      # NLP query parser & formatter
│   ├── prolog_engine.py      # pyswip Prolog wrapper
│   └── aiml_engine.py        # python-aiml wrapper
│
├── assets/                   # Images / icons (optional)
└── screenshots/              # UI screenshots
```

---

## 🧠 Prolog Knowledge Base

### Fact Types (5 distinct types)

| # | Predicate | Description | Example |
|---|-----------|-------------|---------|
| 1 | `male/1` | Male family members | `male(ali).` |
| 2 | `female/1` | Female family members | `female(laiba).` |
| 3 | `parent/2` | Parent-child relationship | `parent(ali, zain).` |
| 4 | `husband/2` | Husband-wife relationship | `husband(ali, alia).` |
| 5 | `wife/2` | Wife-husband relationship | `wife(alia, ali).` |

### Rules (36 rules)

| Category | Rules |
|----------|-------|
| Basic | father, mother, son, daughter, sibling |
| Siblings | brother, sister, spouse |
| Grandparents | grandparent, grandfather, grandmother, grandchild, grandson, granddaughter |
| Extended | uncle, aunt, cousin, nephew, niece |
| Eastern | chacha, phoophi, maamu, khala |
| Eastern GP | dada, dadi, nana, nani |
| In-laws | father_in_law, mother_in_law, brother_in_law, sister_in_law |
| Step | step_father, step_mother |
| Lineage | ancestor, descendant, family_member |

---

## 👨‍👩‍👧‍👦 Family Tree

```
Shakeel ─── Shakeela
    │           │
   Ali ────── Alia
    │           │
   Zain       Zaini
   
   Shakeel ─── Shakeela
        │          │
       Asad ──── Sana
        │          │
      Laiba      Hamza
      
   Usman ─── Nadia
```

**Males:** Ali, Asad, Shakeel, Zain, Usman, Hamza  
**Females:** Alia, Shakeela, Zaini, Laiba, Sana, Nadia

---

## 💬 AIML Patterns

The AIML file handles:
- **Greetings:** hi, hello, hey, salaam, assalam o alaikum
- **Small talk:** how are you, what is your name, who are you, are you a robot
- **Help:** help, examples, what can you do, how do you work
- **Farewells:** bye, goodbye, see you, thank you
- **Fallback:** generic catch-all for unrecognized input

---

## 🐍 Python Query Handler

The `QueryHandler` class in `utils/query_handler.py` intelligently parses natural language:

```python
qh = QueryHandler()

result = qh.parse("can you tell me who the grandfather of zain is")
# {
#   "is_relation_query" : True,
#   "relation"          : "grandfather",
#   "prolog_relation"   : "grandfather",
#   "person"            : "zain",
#   "prolog_query"      : "grandfather(X, zain)",
#   "error"             : None
# }
```

**Parsing pipeline:**
1. Normalize (lowercase, strip punctuation)
2. Detect relation (longest-match from `RELATION_MAP`)
3. Extract person name (`of <name>` pattern → known names → last meaningful word)
4. Build Prolog query string

---

## 🚀 Setup & Run

### Prerequisites

1. **Python 3.9+**
2. **SWI-Prolog** — must be installed on your system

   **Windows:** Download from [swi-prolog.org](https://www.swi-prolog.org/download/stable)  
   **Ubuntu/Debian:** `sudo apt-get install swi-prolog`  
   **macOS:** `brew install swi-prolog`

### Installation

```bash
# 1. Clone or download the project
git clone <your-repo-url>
cd family_chatbot

# 2. Create virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 🎯 Example Queries

| Query | Relation Detected | Answer |
|-------|-------------------|--------|
| `father of ali` | father | Shakeel |
| `who is mother of zain` | mother | Alia |
| `grandfather of zain` | grandfather | Shakeel |
| `can you tell me grandfather of laiba` | grandfather | Shakeel |
| `chacha of laiba` | chacha | Ali |
| `dada of zain` | dada | Shakeel |
| `brother of ali` | brother | Asad |
| `cousin of zain` | cousin | Laiba, Hamza |
| `ancestor of laiba` | ancestor | Asad, Sana, Shakeel, Shakeela |

---

## 🏗️ Architecture

```
User Input (Natural Language)
        │
        ▼
  QueryHandler.parse()          ← Python NLP
  (normalize → detect relation → extract name → build query)
        │
        ├─── Relation found? ──YES──► PrologEngine.query()  ← Symbolic AI
        │                                    │
        │                              Prolog searches family.pl
        │                                    │
        │                              Return results
        │
        └─── No relation? ──────────► AIMLEngine.respond()  ← Pattern matching
                                             │
                                       AIML pattern match
                                             │
                                       Return response
        │
        ▼
  Streamlit UI  ← Display formatted answer with source badge
```

---

## 📚 Technologies Used

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Core language |
| Streamlit | ≥1.32 | Web UI |
| pyswip | ≥0.2.10 | Python-Prolog bridge |
| python-aiml | ≥0.9.2 | AIML processing |
| SWI-Prolog | Latest | Prolog runtime |

---

## ✅ Assignment Checklist

- [x] Prolog knowledge base with **5 fact types**
- [x] Prolog knowledge base with **36 rules** (> 30 required)
- [x] AIML chatbot with custom `.aiml` file
- [x] AIML handles greetings, small talk, and generic responses
- [x] Python middleware layer (intelligent NLP parsing)
- [x] Streamlit web interface
- [x] Handles **all natural language variations** of queries
- [x] Modular, professional project structure
- [x] GitHub-ready with README

---

## 👨‍💻 Author

**Muhammad Mudassar**  
University of Management and Technology (UMT)  
AI 473 — Artificial Neural Networks & Deep Learning  
Spring 2026
