import streamlit as st
from modules.dashboard import show_dashboard
from modules.invoice_processor import show_invoice_processor
from modules.decision_agent import show_decision_agent

st.set_page_config(
    page_title="Financial Ops AI",
    page_icon="💼",
    layout="wide"
)

def show_home():
    # Hero Section
    st.markdown("""
        <h1 style='text-align: center; font-size: 3em;'>💼 Financial Ops AI</h1>
        <p style='text-align: center; font-size: 1.3em; color: gray;'>
            Intelligent back-office automation for asset recovery companies
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Three feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Business Dashboard")
        st.markdown("""
        - Real-time KPI metrics
        - Recovery rate tracking
        - Case status breakdown
        - Industry performance charts
        """)

    with col2:
        st.markdown("### 🧾 Invoice Processor")
        st.markdown("""
        - Upload PDF, image, or text invoices
        - AI vision reads real photos of receipts
        - Extracts client, amount, dates, status
        - Powered by Groq Llama 4 Vision
        """)

    with col3:
        st.markdown("### 🤖 Decision Agent")
        st.markdown("""
        - AI-powered case analysis
        - Recommends next actions
        - Urgency scoring system
        - Per-case deep dive view
        """)

    st.markdown("---")

    # Stats bar
    st.markdown("### 📈 System Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Modules", "3")
    col2.metric("Cases Tracked", "15")
    col3.metric("Invoices Processed", "10")
    col4.metric("AI Recommendations", "15")

    st.markdown("---")
    st.markdown("""
        <p style='text-align: center; color: gray;'>
            Built with Python · Streamlit · Pandas · Plotly
        </p>
    """, unsafe_allow_html=True)


# --- Sidebar Navigation ---
st.sidebar.title("💼 Financial Ops AI")
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "📊 Dashboard", "🧾 Invoice Processor", "🤖 Decision Agent"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("Built with Python + Streamlit")

# --- Page Routing ---
if page == "🏠 Home":
    show_home()
elif page == "📊 Dashboard":
    show_dashboard()
elif page == "🧾 Invoice Processor":
    show_invoice_processor()
elif page == "🤖 Decision Agent":
    show_decision_agent()