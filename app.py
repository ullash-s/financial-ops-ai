import streamlit as st
from modules.dashboard import show_dashboard
from modules.invoice_processor import show_invoice_processor
from modules.decision_agent import show_decision_agent

st.set_page_config(
    page_title="Financial Ops AI",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI-Powered Financial Operations System")
st.markdown("#### Intelligent back-office automation for asset recovery")

page = st.sidebar.selectbox(
    "Navigate",
    ["📊 Dashboard", "🧾 Invoice Processor", "🤖 Decision Agent"]
)

if page == "📊 Dashboard":
    show_dashboard()
elif page == "🧾 Invoice Processor":
    show_invoice_processor()
elif page == "🤖 Decision Agent":
    show_decision_agent()