import streamlit as st
import sqlite3
from datetime import datetime
import json

# Page Configuration
st.set_page_config(
    page_title="Amit Thori Enterprises",
    page_icon="💼",
    layout="centered"
)

# --- PWA CONFIGURATION (RENDER REAL APP SETUP) ---
manifest_data = {
    "name": "Amit Thori Enterprises",
    "short_name": "Amit Thori",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#FDFBF7",
    "theme_color": "#D4AF37",
    "icons": [
        {
            "src": "https://img.icons8.com/color/192/briefcase.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "https://img.icons8.com/color/512/briefcase.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

manifest_json_str = json.dumps(manifest_data)

st.markdown(f"""
    <link rel="manifest" href='data:application/manifest+json,{manifest_json_str}'>
    <link rel="apple-touch-icon" href="https://img.icons8.com/color/192/briefcase.png">
    <meta name="theme-color" content="#D4AF37">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)

# --- LUXURY CSS WITH CLEAR BUTTON TEXT ---
st.markdown("""
<style>
    /* STREAMLIT DEFAULT INTERFACE HIDE */
    #MainMenu {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden; display: none !important;}

    .stApp {
        background-color: #FDFBF7;
        color: #1F1B18;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header-box {
        text-align: center;
        padding: 20px 10px;
        border-bottom: 1.5px solid #EDE6D8;
        margin-bottom: 25px;
    }
    .main-title {
        color: #1F1B18;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #D4AF37;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .metric-card {
        background: #FFFFFF;
        border: 1.2px solid #D4AF37;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.08);
    }
    .metric-label {
        font-size: 12px;
        color: #82786F;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-val-work {
        font-size: 18px;
        font-weight: 700;
        color: #2E7D32;
    }
    .metric-val-pay {
        font-size: 18px;
        font-weight: 700;
        color: #C62828;
    }
    .metric-val-net {
        font-size: 18px;
        font-weight: 700;
        color: #D4AF37;
    }
    .record-card {
        background: #FFFFFF;
        border: 1px solid #EDE6D8;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    /* BUTTON STYLING */
    div.stButton > button:first-child {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        height: 50px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(212, 175, 55, 0.25) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #B8972E !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- OFFLINE SQLITE DATABASE ---
def init_db():
    conn = sqlite3.connect("amit_thori_ledger.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_name TEXT NOT NULL,
            amount REAL NOT NULL,
            entry_type TEXT NOT NULL,
            work_description TEXT,
            record_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- HEADER SECTION ---
st.markdown("""
<div class="header-box">
    <div class="main-title">AMIT THORI ENTERPRISES</div>
    <div class="sub-title">Powered by AURUM AI (Kuldeep Guleria)</div>
</div>
""", unsafe_allow_html=True)

# --- TOTALS METRICS ---
conn = sqlite3.connect("amit_thori_ledger.db")
c = conn.cursor()
c.execute("SELECT entry_type, SUM(amount) FROM ledger GROUP BY entry_type")
totals = dict(c.fetchall())
conn.close()

total_work = totals.get("WORK_LOGGED", 0.0)
total_paid = totals.get("PAYMENT_MADE", 0.0)
net_balance = total_work - total_paid

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Work Value</div>
        <div class="metric-val-work">INR {total_work:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Payouts</div>
        <div class="metric-val-pay">INR {total_paid:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Net Payable</div>
        <div class="metric-val-net">INR {net_balance:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --- ACTION INPUT BOX ---
with st.container():
    c_name, c_amt = st.columns([1.5, 1])
    with c_name:
        worker_name = st.text_input("Worker Name", placeholder="e.g. Ramesh Kumar")
    with c_amt:
        amount = st.number_input("Amount (INR)", min_value=0.0, step=50.0, format="%.2f")

    task_note = st.text_input("Task / Note", placeholder="e.g. 50pcs cutting, weekly advance")

    btn_work, btn_pay = st.columns(2)
    with btn_work:
        if st.button("➕ LOG WORK (Earned)", key="btn_work", use_container_width=True):
            if worker_name.strip() and amount > 0:
                conn = sqlite3.connect("amit_thori_ledger.db")
                c = conn.cursor()
                dt = datetime.now().strftime("%d %b %Y, %I:%M %p")
                c.execute("INSERT INTO ledger (worker_name, amount, entry_type, work_description, record_date) VALUES (?, ?, ?, ?, ?)",
                          (worker_name.strip(), amount, "WORK_LOGGED", task_note if task_note.strip() else "Standard Work", dt))
                conn.commit()
                conn.close()
                st.rerun()

    with btn_pay:
        if st.button("➖ MAKE PAYOUT (Paid)", key="btn_pay", use_container_width=True):
            if worker_name.strip() and amount > 0:
                conn = sqlite3.connect("amit_thori_ledger.db")
                c = conn.cursor()
                dt = datetime.now().strftime("%d %b %Y, %I:%M %p")
                c.execute("INSERT INTO ledger (worker_name, amount, entry_type, work_description, record_date) VALUES (?, ?, ?, ?, ?)",
                          (worker_name.strip(), amount, "PAYMENT_MADE", task_note if task_note.strip() else "Cash Advance", dt))
                conn.commit()
                conn.close()
                st.rerun()

st.divider()

# --- RECORDS TABS ---
tab_all, tab_work, tab_pay = st.tabs(["All Records", "Work Entries", "Disbursements"])

def show_records(filter_type=None):
    conn = sqlite3.connect("amit_thori_ledger.db")
    c = conn.cursor()
    if filter_type:
        c.execute("SELECT worker_name, amount, entry_type, work_description, record_date FROM ledger WHERE entry_type = ? ORDER BY id DESC", (filter_type,))
    else:
        c.execute("SELECT worker_name, amount, entry_type, work_description, record_date FROM ledger ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("No records available in this view.")
        return

    for name, amt, etype, note, dt in rows:
        is_work = (etype == "WORK_LOGGED")
        color = "#2E7D32" if is_work else "#C62828"
        prefix = "+" if is_work else "-"
        tag = "Work Logged" if is_work else "Cash Disbursed"

        st.markdown(f"""
        <div class="record-card">
            <div>
                <b style="font-size:15px; color:#1F1B18;">{name}</b><br>
                <small style="color:#82786F;">{tag} | {dt}</small><br>
                <small style="color:#A1978B;">{note}</small>
            </div>
            <div style="font-size:16px; font-weight:700; color:{color};">
                {prefix}INR {amt:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_all:
    show_records()

with tab_work:
    show_records("WORK_LOGGED")

with tab_pay:
    show_records("PAYMENT_MADE")
