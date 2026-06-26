"""
🛡️ GARUDA AI — Intelligent Conversational Crime Intelligence & Analytics Platform
Powered by Google Vertex AI (Gemini 2.0 Flash)
Hackathon Submission: AI Camp 2026
GCP Project: aicamp26062026
"""
import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from fpdf import FPDF
import base64
from datetime import datetime
import streamlit.components.v1 as components
import json

# =====================================================================
# PAGE CONFIG & PREMIUM CSS
# =====================================================================
st.set_page_config(
    page_title="GARUDA AI | Crime Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* Karnataka Police Inspired Theme: Warm Cream, Maroon, Gold, Navy */
.main {
    background: linear-gradient(160deg, #fdf8f0 0%, #f5ede3 50%, #faf6f1 100%);
    color: #2c1810;
    font-family: 'Inter', sans-serif;
}

/* Headers: Deep Maroon gradient (Karnataka emblem) */
h1, h2, h3 {
    background: linear-gradient(90deg, #7b1a2c, #9b2335, #b8860b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c1810 0%, #3d1f15 40%, #4a2518 100%) !important;
}
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}
section[data-testid="stSidebar"] * {
    color: #f5ede3 !important;
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    background: linear-gradient(90deg, #e8c36a, #f0d77a) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
section[data-testid="stSidebar"] div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(232, 195, 106, 0.3) !important;
    border-radius: 10px;
}
section[data-testid="stSidebar"] div[data-testid="stMetric"] label {
    color: #e8c36a !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(232, 195, 106, 0.2) !important;
}
section[data-testid="stSidebar"] .stSelectbox label {
    color: #e8c36a !important;
}
section[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, #9b2335, #7b1a2c) !important;
    border: 1px solid rgba(232, 195, 106, 0.3) !important;
}

/* Tabs: Navy base with maroon active */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    height: 48px;
    background-color: rgba(27, 42, 74, 0.08);
    border-radius: 8px 8px 0 0;
    color: #4a3728;
    font-weight: 600;
    padding: 10px 20px;
    border: 1px solid rgba(123, 26, 44, 0.1);
}
.stTabs [aria-selected="true"] {
    background-color: rgba(123, 26, 44, 0.08) !important;
    color: #7b1a2c !important;
    border-bottom: 3px solid #9b2335 !important;
}

/* Buttons: Maroon-Gold gradient (Police badge colors) */
.stButton>button {
    background: linear-gradient(135deg, #7b1a2c 0%, #9b2335 60%, #b8860b 100%);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 4px 14px 0 rgba(123, 26, 44, 0.3);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px 0 rgba(123, 26, 44, 0.45);
    background: linear-gradient(135deg, #5c1320 0%, #7b1a2c 60%, #a07508 100%);
}

/* Metric cards: Light with gold border */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(184, 134, 11, 0.25);
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 8px rgba(123, 26, 44, 0.06);
}
div[data-testid="stMetric"] label {
    color: #4a3728 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #7b1a2c !important;
}

/* Card class: Warm white with subtle maroon border */
.card {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(123, 26, 44, 0.12);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(44, 24, 16, 0.06);
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(123, 26, 44, 0.08);
    border-radius: 10px;
}

/* Expander styling */
details {
    background: rgba(255, 255, 255, 0.5) !important;
    border: 1px solid rgba(184, 134, 11, 0.15) !important;
    border-radius: 8px !important;
}

/* Dataframe container */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(123, 26, 44, 0.1);
    border-radius: 8px;
}

/* Selectbox & inputs */
div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.8) !important;
    border-color: rgba(123, 26, 44, 0.2) !important;
}

/* Links */
a { color: #7b1a2c !important; }
a:hover { color: #b8860b !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# DATABASE & VERTEX AI INITIALIZATION
# =====================================================================
DB_PATH = "crime_database.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def query_db(sql_query, params=()):
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(sql_query, conn, params=params)
        return df
    except Exception as e:
        raise e
    finally:
        conn.close()

# Vertex AI Configuration
PROJECT_ID = os.environ.get("GCP_PROJECT", "aicamp26062026")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

@st.cache_resource
def init_gemini():
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        # Use Gemini 2.0 Flash for fast + accurate responses
        return GenerativeModel("gemini-2.0-flash-001")
    except Exception:
        try:
            # Fallback to Gemini 1.5 Flash if 2.0 not available
            return GenerativeModel("gemini-1.5-flash-001")
        except Exception as e:
            st.error(f"⚠️ Vertex AI init failed: {e}")
            return None

gemini_model = init_gemini()

# =====================================================================
# DATABASE SCHEMA (for LLM context)
# =====================================================================
DB_SCHEMA = """
Table `neighborhoods`:
- name (TEXT PRIMARY KEY) - e.g. 'Koramangala', 'Indiranagar', 'Jayanagar', 'Majestic', 'Kalyan Nagar', 'Peenya', 'Shivaji Nagar', 'Whitefield', 'Electronic City', 'Hebbal', 'Yelahanka', 'Banashankari'
- unemployment_rate (REAL), poverty_rate (REAL), youth_recreation_centers (INTEGER)
- police_patrol_density (TEXT) - 'High', 'Medium', 'Low'
- latitude (REAL), longitude (REAL)

Table `firs`:
- fir_id (TEXT PRIMARY KEY) - Format 'FIR-2026-2XXX'
- crime_type (TEXT) - 'Burglary', 'Robbery', 'Narcotics Sale', 'Assault', 'Cyber Fraud', 'Extortion', 'Vehicle Theft', 'Murder'
- date (TEXT 'YYYY-MM-DD'), time (TEXT 'HH:MM')
- location (TEXT), neighborhood (TEXT REFERENCES neighborhoods.name)
- modus_operandi (TEXT), status (TEXT) - 'Under Investigation', 'Chargesheeted', 'Arrested', 'Closed', 'Cold Case'
- severity (TEXT) - 'Low', 'Medium', 'High', 'Critical'
- financial_loss (REAL), event_context (TEXT), details_en (TEXT), details_kn (TEXT)

Table `offenders`:
- offender_id (TEXT PRIMARY KEY), name (TEXT), age (INTEGER), gender (TEXT)
- criminal_history (TEXT), status (TEXT), gang_affiliation (TEXT) - 'Majestic Boys', 'Cyber Syndicate 404', 'Kalyan Nagar Syndicate', 'None'
- typical_mo (TEXT), risk_score (INTEGER 1-10), bank_account (TEXT)

Table `victims`:
- victim_id (TEXT PRIMARY KEY), name (TEXT), age (INTEGER), gender (TEXT), occupation (TEXT)

Table `fir_offenders`:
- fir_id (TEXT), offender_id (TEXT), role (TEXT) - 'Mastermind', 'Executor', 'Lookout', 'Accomplice'

Table `fir_victims`:
- fir_id (TEXT), victim_id (TEXT)

Table `financial_transactions`:
- transaction_id (TEXT PRIMARY KEY), fir_id (TEXT)
- sender_account (TEXT), receiver_account (TEXT), amount (REAL), date (TEXT)
- transaction_type (TEXT) - 'UPI Transfer', 'Cash Deposit', 'NEFT', 'Hawala', 'Crypto'

RELATIONS:
- firs.neighborhood = neighborhoods.name
- fir_offenders.fir_id = firs.fir_id, fir_offenders.offender_id = offenders.offender_id
- fir_victims.fir_id = firs.fir_id, fir_victims.victim_id = victims.victim_id
- financial_transactions.fir_id = firs.fir_id
- financial_transactions.sender_account/receiver_account can JOIN with offenders.bank_account
"""

# =====================================================================
# HELPER: Voice I/O Components (Web Speech API)
# =====================================================================
def get_stt_component(lang_default="en-IN"):
    return f"""
    <div style="background:rgba(27,42,74,0.05);padding:15px;border-radius:12px;border:1px solid rgba(123,26,44,0.15);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#2c1810;font-weight:600;font-size:14px;">🎙️ Voice Input</span>
            <select id="voice-lang" style="background:#fdf8f0;color:#2c1810;border:1px solid rgba(123,26,44,0.3);border-radius:5px;padding:4px;">
                <option value="en-IN" {'selected' if lang_default=='en-IN' else ''}>English</option>
                <option value="kn-IN" {'selected' if lang_default=='kn-IN' else ''}>ಕನ್ನಡ</option>
            </select>
        </div>
        <div style="display:flex;gap:10px;align-items:center;">
            <button id="mic-btn" onclick="startRec()" style="background:linear-gradient(135deg,#7b1a2c,#9b2335);color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-weight:bold;">🔴 Record</button>
            <span id="mic-status" style="color:#4a3728;font-size:13px;">Ready</span>
        </div>
        <div id="transcript" style="margin-top:10px;padding:10px;background:rgba(255,255,255,0.6);border-radius:6px;color:#2c1810;min-height:30px;font-size:14px;border:1px solid rgba(123,26,44,0.1);"></div>
    </div>
    <script>
    function startRec() {{
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {{
            document.getElementById('mic-status').innerText = 'Not supported in this browser';
            return;
        }}
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        const r = new SR();
        r.lang = document.getElementById('voice-lang').value;
        r.continuous = false; r.interimResults = false;
        r.onstart = () => {{ document.getElementById('mic-status').innerText = 'Listening...'; document.getElementById('mic-btn').style.background = 'linear-gradient(135deg,#dc2626,#b91c1c)'; }};
        r.onend = () => {{ document.getElementById('mic-btn').style.background = 'linear-gradient(135deg,#7b1a2c,#9b2335)'; }};
        r.onresult = (e) => {{
            const t = e.results[0][0].transcript;
            document.getElementById('transcript').innerText = t;
            document.getElementById('mic-status').innerText = 'Done! Copy text to chat.';
            const url = new URL(window.parent.location.href);
            url.searchParams.set('voice_query', t);
            window.parent.location.href = url.toString();
        }};
        r.onerror = (e) => {{ document.getElementById('mic-status').innerText = 'Error: ' + e.error; }};
        r.start();
    }}
    </script>
    """

def run_tts(text, lang="en-IN"):
    safe = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")[:500]
    components.html(f"""<script>
    const u = new SpeechSynthesisUtterance('{safe}');
    u.lang = '{lang}'; window.speechSynthesis.speak(u);
    </script>""", height=0, width=0)

# =====================================================================
# HELPER: PDF Export
# =====================================================================
def clean_pdf_text(text):
    return "".join(i for i in text if ord(i) < 128)

class ConversationPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'GARUDA AI - Crime Intelligence Report', align='C', ln=True)
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 5, 'Crime Intelligence Report | Confidential', align='C', ln=True)
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()} | Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | Project: aicamp26062026', align='C')

def generate_pdf_link(history):
    pdf = ConversationPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "Investigation Dialogue Transcript", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.ln(4)
    for msg in history:
        role = "INVESTIGATOR" if msg["role"] == "user" else "GARUDA AI"
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 6, f"[{role}]", ln=True)
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 5, clean_pdf_text(msg["content"][:800]))
        if "sql" in msg:
            pdf.set_font("Helvetica", 'I', 8)
            pdf.multi_cell(0, 4, f"SQL: {msg['sql'][:200]}")
        pdf.ln(3)
    b64 = base64.b64encode(pdf.output(dest='S')).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="Garuda_Intel_Report.pdf"><button style="background:linear-gradient(135deg,#7b1a2c,#9b2335);color:white;border:none;padding:8px 16px;border-radius:6px;font-weight:bold;cursor:pointer;">📥 Download PDF Report</button></a>'

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown("## 🛡️ GARUDA AI")
    st.caption("Intelligent Crime Intelligence & Analytics Platform")
    st.divider()

    try:
        total_firs = query_db("SELECT COUNT(*) as c FROM firs").iloc[0]['c']
        total_offenders = query_db("SELECT COUNT(*) as c FROM offenders").iloc[0]['c']
        total_neighborhoods = query_db("SELECT COUNT(*) as c FROM neighborhoods").iloc[0]['c']
        total_loss = query_db("SELECT COALESCE(SUM(financial_loss),0) as c FROM firs").iloc[0]['c']
        open_cases = query_db("SELECT COUNT(*) as c FROM firs WHERE status='Under Investigation'").iloc[0]['c']
    except:
        total_firs = total_offenders = total_neighborhoods = open_cases = 0
        total_loss = 0

    st.markdown("### 📊 Database Overview")
    c1, c2 = st.columns(2)
    c1.metric("FIRs", total_firs)
    c2.metric("Suspects", total_offenders)
    c1.metric("Sectors", total_neighborhoods)
    c2.metric("Open Cases", open_cases)
    st.metric("Total Financial Loss", f"₹{total_loss/100000:.1f} Lakh")

    st.divider()
    st.markdown("### ⚙️ Settings")
    selected_lang = st.selectbox("Interface Language", ["English", "ಕನ್ನಡ (Kannada)"])

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()
    st.caption("**Engine:** Gemini 2.0 Flash (Vertex AI)")
    st.caption("**Project:** aicamp26062026")
    st.caption("**Region:** us-central1")

# =====================================================================
# MAIN HEADER & SESSION STATE
# =====================================================================
st.markdown("# 🛡️ GARUDA AI: Intelligent Crime Analytics Platform")
st.caption("Conversational AI | Criminal Network Analysis | Trend Intelligence | Predictive Insights")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""

# Handle voice query from URL params
url_voice = st.query_params.get("voice_query", "")
if url_voice:
    st.session_state.voice_input = url_voice
    st.query_params.clear()

# =====================================================================
# TAB LAYOUT
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ Conversational Intelligence",
    "🕸️ Criminal Network Analysis",
    "📊 Crime Trends & Hotspots",
    "🕵️ MO Matcher & Predictive Intel"
])

# =====================================================================
# TAB 1: CONVERSATIONAL INTELLIGENCE
# =====================================================================
with tab1:
    st.subheader("💬 Natural Language Crime Database Interface")
    st.write("Ask questions in **English** or **ಕನ್ನಡ**. Garuda translates to SQL, queries the database, and provides criminological analysis.")

    chat_col, assist_col = st.columns([2.5, 1])

    with assist_col:
        st.markdown("#### 🎙️ Voice Input")
        components.html(get_stt_component("kn-IN" if "ಕನ್ನಡ" in selected_lang else "en-IN"), height=180)

        st.markdown("#### 💡 Sample Queries")
        samples = [
            "Show all cyber fraud cases in Koramangala",
            "Which gang has the most members?",
            "List cold cases with financial loss > 5 lakh",
            "ಮೆಜೆಸ್ಟಿಕ್‌ನಲ್ಲಿ ಎಷ್ಟು ಸುಲಿಗೆ ಪ್ರಕರಣಗಳಿವೆ?",
            "ಯಾವ ಆರೋಪಿಗಳು ಪುನರಾವರ್ತಿತ ಅಪರಾಧಿಗಳು?",
            "Find offenders linked to Kalyan Nagar Syndicate",
            "Show crimes during Dasara Festival",
        ]
        for idx, s in enumerate(samples):
            if st.button(s, key=f"sample_{idx}", use_container_width=True):
                st.session_state.voice_input = s
                st.rerun()

        with st.expander("🗄️ Database Schema"):
            st.code(DB_SCHEMA, language="sql")

    with chat_col:
        # Display chat history
        chat_container = st.container(height=420)
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.chat_message("user", avatar="🕵️").write(msg["content"])
                else:
                    st.chat_message("assistant", avatar="🤖").write(msg["content"])
                    if "sql" in msg and msg["sql"]:
                        with st.expander("🔧 SQL Executed"):
                            st.code(msg["sql"], language="sql")
                    if "data" in msg and msg["data"] is not None:
                        with st.expander("📋 Result Data", expanded=True):
                            st.dataframe(msg["data"], use_container_width=True, hide_index=True)

        # Chat Input
        user_input = st.chat_input("Ask about crimes, suspects, victims, locations...")
        query_to_run = user_input if user_input else (st.session_state.voice_input if st.session_state.voice_input else None)

        if query_to_run:
            st.session_state.voice_input = ""
            st.session_state.chat_history.append({"role": "user", "content": query_to_run})

            with st.spinner("🔍 Garuda AI analyzing..."):
                sql_query = ""
                db_results = None
                analysis = ""

                # Build context from recent conversation for follow-ups
                recent_context = ""
                if len(st.session_state.chat_history) > 2:
                    last_msgs = st.session_state.chat_history[-4:-1]
                    recent_context = "\n".join([f"{m['role']}: {m['content'][:150]}" for m in last_msgs])

                # Step 1: NL to SQL via Gemini
                sql_prompt = f"""You are an expert SQLite query generator. Convert the user's natural language question into a valid SQLite query.
RULES:
- Output ONLY the raw SQL query. No markdown, no explanations, no code blocks.
- Use the exact table/column names from the schema.
- For Kannada queries, understand the intent and generate SQL for the English schema.
- Consider conversation context for follow-up questions.

DATABASE SCHEMA:
{DB_SCHEMA}

CONVERSATION CONTEXT (for follow-ups):
{recent_context}

USER QUERY: "{query_to_run}"

SQL:"""

                try:
                    if gemini_model:
                        sql_raw = gemini_model.generate_content(sql_prompt, generation_config={"temperature": 0.0}).text.strip()
                        sql_query = sql_raw.replace("```sql", "").replace("```", "").replace("SQL:", "").strip()
                        db_results = query_db(sql_query)
                except Exception as e:
                    st.warning(f"SQL generation issue: {e}. Attempting fallback...")
                    try:
                        sql_query = f"SELECT * FROM firs WHERE details_en LIKE '%{query_to_run.split()[0]}%' LIMIT 10"
                        db_results = query_db(sql_query)
                    except:
                        db_results = pd.DataFrame()

                # Step 2: Criminological Analysis
                result_str = db_results.head(20).to_string() if db_results is not None and not db_results.empty else "No results found."
                lang_hint = "Respond in Kannada if the query was in Kannada. Otherwise English." if any(ord(c) > 3000 for c in query_to_run) else "Respond in English."

                analysis_prompt = f"""You are GARUDA AI, a Principal Criminologist and Intelligence Analyst.

Analyze the investigator's query and database results. Provide:
1. **Summary**: Clear findings in natural language.
2. **Criminological Insight**: Ground analysis in theories (Strain Theory, Social Disorganization, Routine Activity Theory, Differential Association).
3. **Actionable Recommendations**: 2-3 proactive steps for investigators.

Query: "{query_to_run}"
SQL Used: {sql_query}
Database Results:
{result_str}

{lang_hint}
Keep response concise but insightful (under 300 words)."""

                try:
                    if gemini_model:
                        analysis = gemini_model.generate_content(analysis_prompt).text
                    else:
                        analysis = f"Found {len(db_results) if db_results is not None else 0} matching records."
                except Exception as e:
                    analysis = f"Analysis error: {e}"

                # Save to history
                msg_payload = {"role": "assistant", "content": analysis, "sql": sql_query}
                if db_results is not None and not db_results.empty:
                    msg_payload["data"] = db_results
                st.session_state.chat_history.append(msg_payload)
                st.rerun()

        # Action buttons
        if st.session_state.chat_history:
            st.divider()
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                last_asst = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
                if last_asst:
                    is_kn = any(ord(c) > 3000 for c in last_asst[-1]["content"][:100])
                    if st.button("🔊 Speak Response"):
                        run_tts(last_asst[-1]["content"], "kn-IN" if is_kn else "en-IN")
            with ac2:
                st.markdown(generate_pdf_link(st.session_state.chat_history), unsafe_allow_html=True)
            with ac3:
                if st.button("📊 Visualize Last Result"):
                    last_data_msg = [m for m in st.session_state.chat_history if "data" in m]
                    if last_data_msg:
                        df = last_data_msg[-1]["data"]
                        if "crime_type" in df.columns:
                            fig = px.bar(df['crime_type'].value_counts().reset_index(), x='crime_type', y='count', template="seaborn")
                            st.plotly_chart(fig, use_container_width=True)
                        elif "neighborhood" in df.columns:
                            fig = px.bar(df['neighborhood'].value_counts().reset_index(), x='neighborhood', y='count', template="seaborn")
                            st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# TAB 2: CRIMINAL NETWORK ANALYSIS
# =====================================================================
with tab2:
    st.subheader("🕸️ Criminal Network & Relationship Analysis")
    st.write("Discover hidden links between suspects, gangs, crimes, financial accounts, and victims.")

    # Suspect selector
    try:
        suspects_df = query_db("SELECT offender_id, name, gang_affiliation, risk_score FROM offenders ORDER BY risk_score DESC")
        options = {"ALL": "🌐 Full Network View"}
        for _, r in suspects_df.iterrows():
            options[r['offender_id']] = f"{r['name']} | {r['gang_affiliation']} | Risk: {r['risk_score']}/10"
    except:
        options = {"ALL": "Full Network"}

    sel_suspect = st.selectbox("🎯 Focus on Suspect:", list(options.keys()), format_func=lambda x: options[x])

    net_col, detail_col = st.columns([2, 1])

    with net_col:
        def build_network(target="ALL"):
            off_df = query_db("SELECT offender_id, name, gang_affiliation, bank_account, risk_score FROM offenders")
            fir_df = query_db("SELECT fir_id, crime_type, neighborhood, severity FROM firs")
            fir_off = query_db("SELECT fir_id, offender_id, role FROM fir_offenders")
            fir_vic = query_db("SELECT fir_id, victim_id FROM fir_victims")
            vic_df = query_db("SELECT victim_id, name FROM victims")
            tx_df = query_db("SELECT sender_account, receiver_account, amount FROM financial_transactions")

            G = nx.Graph()
            colors, sizes, hovers = {}, {}, {}

            if target != "ALL":
                related_firs = fir_off[fir_off['offender_id'] == target]['fir_id'].tolist()
                co_accused = fir_off[fir_off['fir_id'].isin(related_firs)]['offender_id'].unique().tolist()
                off_df = off_df[off_df['offender_id'].isin(co_accused)]
                fir_off = fir_off[fir_off['offender_id'].isin(co_accused)]
                related_firs = fir_off['fir_id'].unique().tolist()
                fir_df = fir_df[fir_df['fir_id'].isin(related_firs)]
                fir_vic = fir_vic[fir_vic['fir_id'].isin(related_firs)]
                vic_df = vic_df[vic_df['victim_id'].isin(fir_vic['victim_id'].tolist())]
                accs = off_df['bank_account'].tolist()
                tx_df = tx_df[(tx_df['sender_account'].isin(accs)) | (tx_df['receiver_account'].isin(accs))]

            # Add offender nodes
            for _, r in off_df.iterrows():
                nid = r['offender_id']
                G.add_node(nid)
                colors[nid] = '#9b2335'  # Maroon (suspects)
                sizes[nid] = 18 + r['risk_score'] * 2
                hovers[nid] = f"<b>{r['name']}</b><br>Gang: {r['gang_affiliation']}<br>Risk: {r['risk_score']}/10"
                if r['gang_affiliation'] != 'None':
                    gang = r['gang_affiliation']
                    G.add_node(gang)
                    colors[gang] = '#b8860b'  # Gold (gangs)
                    sizes[gang] = 30
                    hovers[gang] = f"<b>Gang: {gang}</b>"
                    G.add_edge(nid, gang)

            # Add FIR nodes
            for _, r in fir_df.iterrows():
                nid = r['fir_id']
                G.add_node(nid)
                colors[nid] = '#1b2a4a'  # Navy (FIRs)
                sizes[nid] = 16
                hovers[nid] = f"<b>{nid}</b><br>{r['crime_type']}<br>{r['neighborhood']}"

            # Add victim nodes
            for _, r in vic_df.iterrows():
                nid = r['victim_id']
                G.add_node(nid)
                colors[nid] = '#2d8659'  # Forest green (victims)
                sizes[nid] = 14
                hovers[nid] = f"<b>Victim: {r['name']}</b>"

            # Edges
            for _, r in fir_off.iterrows():
                if G.has_node(r['fir_id']) and G.has_node(r['offender_id']):
                    G.add_edge(r['fir_id'], r['offender_id'])
            for _, r in fir_vic.iterrows():
                if G.has_node(r['fir_id']) and G.has_node(r['victim_id']):
                    G.add_edge(r['fir_id'], r['victim_id'])

            # Financial edges
            for _, r in tx_df.iterrows():
                s, rv = r['sender_account'], r['receiver_account']
                # Map accounts to offender nodes
                s_off = off_df[off_df['bank_account'] == s]
                r_off = off_df[off_df['bank_account'] == rv]
                if not s_off.empty and not r_off.empty:
                    G.add_edge(s_off.iloc[0]['offender_id'], r_off.iloc[0]['offender_id'])

            if len(G) == 0:
                return go.Figure()

            pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

            edge_x, edge_y = [], []
            for e in G.edges():
                x0, y0 = pos[e[0]]
                x1, y1 = pos[e[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            node_x, node_y, node_c, node_s, node_t = [], [], [], [], []
            for n in G.nodes():
                x, y = pos[n]
                node_x.append(x); node_y.append(y)
                node_c.append(colors.get(n, '#6b4c3b'))
                node_s.append(sizes.get(n, 12))
                node_t.append(hovers.get(n, str(n)))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.8, color='rgba(123,26,44,0.15)'), hoverinfo='none'))
            fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text', text=node_t,
                marker=dict(color=node_c, size=node_s, line=dict(width=1, color='#fdf8f0'))))
            fig.update_layout(showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)', height=500)
            return fig

        try:
            st.plotly_chart(build_network(sel_suspect), use_container_width=True)
        except Exception as e:
            st.error(f"Network error: {e}")

        st.markdown("**Legend:** 🔴 Suspect | 🟡 Gang | 🔵 FIR | 🟢 Victim | Lines = Relationships/Transactions")

    with detail_col:
        st.markdown("#### 💰 Suspicious Financial Flows")
        tx_query = """
        SELECT o1.name as sender, o2.name as receiver, tx.amount, tx.transaction_type, tx.date, f.crime_type
        FROM financial_transactions tx
        JOIN offenders o1 ON tx.sender_account = o1.bank_account
        JOIN offenders o2 ON tx.receiver_account = o2.bank_account
        JOIN firs f ON tx.fir_id = f.fir_id
        """
        if sel_suspect != "ALL":
            tx_query += f" WHERE o1.offender_id = '{sel_suspect}' OR o2.offender_id = '{sel_suspect}'"
        tx_query += " ORDER BY tx.amount DESC LIMIT 15"

        try:
            tx_data = query_db(tx_query)
            if not tx_data.empty:
                st.dataframe(tx_data, use_container_width=True, hide_index=True)
                total_sus = tx_data['amount'].sum()
                st.error(f"⚠️ Total suspicious flow: ₹{total_sus:,.0f}")
            else:
                st.info("No financial links for this selection.")
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("#### 🏴 Organized Crime Groups")
        try:
            gangs = query_db("""
                SELECT gang_affiliation as Gang, COUNT(*) as Members, 
                       ROUND(AVG(risk_score),1) as Avg_Risk, GROUP_CONCAT(name, ', ') as Associates
                FROM offenders WHERE gang_affiliation != 'None' GROUP BY gang_affiliation
            """)
            st.dataframe(gangs, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("#### 🔄 Repeat Offenders")
        try:
            repeats = query_db("""
                SELECT o.name, o.gang_affiliation, COUNT(fo.fir_id) as total_cases, o.risk_score
                FROM offenders o JOIN fir_offenders fo ON o.offender_id = fo.offender_id
                GROUP BY o.offender_id HAVING total_cases > 3 ORDER BY total_cases DESC
            """)
            if not repeats.empty:
                st.dataframe(repeats, use_container_width=True, hide_index=True)
        except:
            pass

# =====================================================================
# TAB 3: CRIME TRENDS & HOTSPOT ANALYTICS
# =====================================================================
with tab3:
    st.subheader("📊 Crime Pattern, Trend & Hotspot Analysis")
    st.write("Examine geographic clusters, seasonal patterns, event-based spikes, and socio-economic crime drivers.")

    try:
        firs_full = query_db("""
            SELECT f.*, n.unemployment_rate, n.poverty_rate, n.youth_recreation_centers, 
                   n.police_patrol_density, n.latitude, n.longitude
            FROM firs f JOIN neighborhoods n ON f.neighborhood = n.name
        """)
    except:
        firs_full = pd.DataFrame()

    if not firs_full.empty:
        # Top metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Critical Cases", len(firs_full[firs_full['severity'] == 'Critical']))
        m2.metric("Avg Loss/Case", f"₹{firs_full['financial_loss'].mean():,.0f}")
        m3.metric("Cold Cases", len(firs_full[firs_full['status'] == 'Cold Case']))
        m4.metric("Top Crime", firs_full['crime_type'].mode().iloc[0] if len(firs_full) > 0 else "N/A")

        # Row 1: Crime type distribution + Geographic hotspot
        r1c1, r1c2 = st.columns(2)

        with r1c1:
            crime_counts = firs_full['crime_type'].value_counts().reset_index()
            crime_counts.columns = ['Crime Type', 'Count']
            fig1 = px.pie(crime_counts, values='Count', names='Crime Type',
                title="Crime Type Distribution", template="seaborn",
                color_discrete_sequence=px.colors.sequential.Burgyl)
            fig1.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
            st.plotly_chart(fig1, use_container_width=True)

        with r1c2:
            sector_data = firs_full.groupby(['neighborhood', 'police_patrol_density']).agg(
                cases=('fir_id', 'count'), total_loss=('financial_loss', 'sum')
            ).reset_index()
            fig2 = px.bar(sector_data, x='neighborhood', y='cases', color='police_patrol_density',
                title="Crime Hotspots by Neighborhood & Patrol Density", template="seaborn",
                color_discrete_map={'High': '#2d8659', 'Medium': '#b8860b', 'Low': '#9b2335'})
            fig2.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
            st.plotly_chart(fig2, use_container_width=True)

        # Row 2: Event-based + Monthly trend
        r2c1, r2c2 = st.columns(2)

        with r2c1:
            event_data = firs_full.groupby('event_context').agg(
                cases=('fir_id', 'count'), avg_loss=('financial_loss', 'mean')
            ).reset_index().sort_values('cases', ascending=False)
            fig3 = px.bar(event_data, x='event_context', y='cases',
                title="Event-Based Crime Spikes (Routine Activity Theory)", template="seaborn",
                color='avg_loss', color_continuous_scale='Reds',
                labels={'event_context': 'Event/Season', 'cases': 'Incidents', 'avg_loss': 'Avg Loss ₹'})
            fig3.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)', showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            firs_full['month'] = pd.to_datetime(firs_full['date']).dt.month_name()
            month_order = ['January', 'February', 'March', 'April', 'May', 'June']
            monthly = firs_full.groupby(['month', 'crime_type']).size().reset_index(name='cases')
            monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
            monthly = monthly.sort_values('month')
            fig4 = px.line(monthly, x='month', y='cases', color='crime_type',
                title="Monthly Crime Trends (Jan-Jun 2026)", template="seaborn", markers=True)
            fig4.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
            st.plotly_chart(fig4, use_container_width=True)

        # Row 3: Socioeconomic correlation + Time of day
        r3c1, r3c2 = st.columns(2)

        with r3c1:
            neigh_stats = firs_full.groupby(['neighborhood', 'poverty_rate', 'unemployment_rate', 'youth_recreation_centers']).size().reset_index(name='crime_count')
            fig5 = px.scatter(neigh_stats, x='poverty_rate', y='crime_count',
                size='crime_count', color='youth_recreation_centers',
                hover_name='neighborhood', trendline="ols",
                title="Strain Theory: Poverty Rate vs Crime (Color=Youth Centers)", template="seaborn",
                labels={'poverty_rate': 'Poverty Rate %', 'crime_count': 'Crimes', 'youth_recreation_centers': 'Youth Centers'})
            fig5.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
            st.plotly_chart(fig5, use_container_width=True)
            st.caption("📌 Higher poverty + fewer youth centers = more crime. Classic Strain Theory validation.")

        with r3c2:
            firs_full['hour'] = firs_full['time'].apply(lambda x: int(x.split(':')[0]) if ':' in str(x) else 0)
            hour_data = firs_full.groupby(['hour', 'crime_type']).size().reset_index(name='cases')
            fig6 = px.area(hour_data, x='hour', y='cases', color='crime_type',
                title="Crime Distribution by Hour of Day", template="seaborn",
                labels={'hour': 'Hour (24h)', 'cases': 'Incidents'})
            fig6.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
            st.plotly_chart(fig6, use_container_width=True)
            st.caption("📌 Routine Activity Theory: Crimes cluster when guardians are absent (late night/early morning).")

        # Row 4: Severity heatmap
        st.markdown("#### 🗺️ Severity Heatmap by Neighborhood")
        heat_data = firs_full.groupby(['neighborhood', 'crime_type']).size().reset_index(name='count')
        heat_pivot = heat_data.pivot_table(index='neighborhood', columns='crime_type', values='count', fill_value=0)
        fig7 = px.imshow(heat_pivot, template="seaborn", aspect="auto",
            title="Crime Type × Neighborhood Heatmap", color_continuous_scale="OrRd")
        fig7.update_layout(plot_bgcolor='rgba(253,248,240,0.5)', paper_bgcolor='rgba(253,248,240,0)')
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.warning("No crime data available. Run the data generator first.")

# =====================================================================
# TAB 4: MO MATCHER & PREDICTIVE INTELLIGENCE
# =====================================================================
with tab4:
    st.subheader("🕵️ Modus Operandi Pattern Matcher & Predictive Intelligence")
    st.write("Input an active case MO. Garuda cross-references the database to find serial patterns, linked suspects, and generates a prevention strategy grounded in criminology.")

    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.markdown("#### 📝 Active Case Details")
        case_mo = st.text_area(
            "Describe the Modus Operandi of the active case:",
            value="Two masked men on a black motorcycle intercepted a delivery executive near a dark underpass. They brandished a knife, snatched his bag containing a laptop and cash, and fled towards the Majestic bus stand area.",
            height=150
        )

        case_area = st.selectbox("Incident Neighborhood:", 
            ["Koramangala", "Indiranagar", "Jayanagar", "Majestic", "Kalyan Nagar", "Peenya", "Shivaji Nagar", "Whitefield", "Electronic City", "Hebbal", "Yelahanka", "Banashankari"])
        
        case_severity = st.select_slider("Estimated Severity:", options=["Low", "Medium", "High", "Critical"], value="High")

        analyze_btn = st.button("🔍 Analyze MO & Generate Intel", use_container_width=True)

    with col_output:
        if analyze_btn and case_mo.strip():
            with st.spinner("🧠 Running deep pattern analysis..."):
                # Fetch all crime MOs for comparison
                all_crimes = query_db("SELECT fir_id, crime_type, neighborhood, modus_operandi, status FROM firs")

                # MO Matching via Gemini
                match_prompt = f"""You are a Crime Pattern Analyst. Compare this active case MO with recorded crimes.

ACTIVE CASE:
MO: "{case_mo}"
Area: {case_area}
Severity: {case_severity}

RECORDED CRIME DATABASE (MO patterns):
{all_crimes.to_string()}

Provide:
1. **Top 5 Most Similar Cases** (by FIR ID) with similarity reasoning.
2. **Suspected Gang/Group** connection if pattern matches known syndicate operations.
3. **Likely Suspect Profile**: Age range, typical behavior, area of operation.
4. **Risk Assessment**: Likelihood of repeat offense (1-10 scale with justification).

Be specific and reference actual FIR IDs from the data."""

                try:
                    if gemini_model:
                        match_result = gemini_model.generate_content(match_prompt).text
                    else:
                        match_result = "Model not available. Manual analysis required."
                except Exception as e:
                    match_result = f"Error: {e}"

                st.markdown("#### 🎯 Pattern Match Results")
                st.info(match_result)

                # Prevention Strategy
                prevention_prompt = f"""You are a Criminologist and Public Safety Strategist for Karnataka State.

For this crime pattern:
MO: "{case_mo}"
Area: {case_area} (Poverty Rate: check socioeconomic profile)

Generate a comprehensive PREVENTION & RESPONSE PLAN:

1. **Criminological Root Cause Analysis** (reference Strain Theory, Routine Activity Theory, Social Disorganization):
   - Why does this crime type occur in this area?
   - What environmental/social factors enable it?

2. **Immediate Tactical Response** (for police):
   - Patrol adjustments
   - Surveillance recommendations
   - Suspect identification priorities

3. **Long-term Social Interventions** (for policymakers):
   - 3 non-policing interventions (youth programs, lighting, CCTV, employment)
   - Community engagement strategies

4. **Predictive Risk Score** for this area (1-10) with justification.

Keep actionable and grounded in evidence-based criminology."""

                try:
                    if gemini_model:
                        prevention_result = gemini_model.generate_content(prevention_prompt).text
                    else:
                        prevention_result = "Strategy generation requires Vertex AI model access."
                except Exception as e:
                    prevention_result = f"Error: {e}"

                st.markdown("#### 🧠 Criminological Prevention Strategy")
                st.success(prevention_result)

                # Show related crimes in the area
                st.markdown("#### 📋 Historical Crimes in This Area")
                area_crimes = query_db(f"SELECT fir_id, crime_type, date, severity, status, modus_operandi FROM firs WHERE neighborhood = '{case_area}' ORDER BY date DESC LIMIT 10")
                if not area_crimes.empty:
                    st.dataframe(area_crimes, use_container_width=True, hide_index=True)

        elif analyze_btn:
            st.warning("Please enter case MO details.")

# =====================================================================
# FOOTER
# =====================================================================
st.divider()
st.markdown("""
<div style="text-align:center; color:#6b4c3b; padding:20px; background:rgba(123,26,44,0.03); border-radius:12px; border:1px solid rgba(123,26,44,0.08);">
    <p style="margin:0;"><strong>🛡️ GARUDA AI</strong> — Intelligent Conversational Crime Intelligence & Analytics Platform</p>
    <p style="margin:4px 0; font-size:0.9em;">Powered by Google Cloud Vertex AI (Gemini 2.0 Flash)</p>
    <p style="margin:4px 0; font-size:0.85em; color:#8b6b5a;">GCP Project: aicamp26062026 | AI Camp Hackathon 2026</p>
</div>
""", unsafe_allow_html=True)
