import streamlit as st
from modules.dashboard import show_dashboard

st.set_page_config(
    page_title="Financial Ops AI",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI-Powered Financial Operations System")
st.markdown("#### Intelligent back-office automation for asset recovery")

# Navigation — we'll expand this as we add more modules
page = st.sidebar.selectbox(
    "Navigate",
    ["📊 Dashboard", "🧾 Invoice Processor", "🤖 Decision Agent"]
)

if page == "📊 Dashboard":
    show_dashboard()
else:
    st.info("🚧 This module is coming soon.")