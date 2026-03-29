import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    """Load cases and invoices from CSV files."""
    cases = pd.read_csv("data/cases.csv")
    invoices = pd.read_csv("data/invoices.csv")
    return cases, invoices

def show_dashboard():
    st.header("📊 Business Operations Dashboard")

    # Load data
    cases, invoices = load_data()

    # --- ROW 1: Key Metrics ---
    # These are the numbers an executive looks at first thing every morning
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    total_owed = cases["amount_owed"].sum()
    total_recovered = cases["amount_recovered"].sum()
    recovery_rate = (total_recovered / total_owed * 100) if total_owed > 0 else 0
    open_cases = len(cases[cases["status"] == "Open"])

    col1.metric("💰 Total Owed", f"${total_owed:,.0f}")
    col2.metric("✅ Total Recovered", f"${total_recovered:,.0f}")
    col3.metric("📈 Recovery Rate", f"{recovery_rate:.1f}%")
    col4.metric("🔓 Open Cases", open_cases)

    st.divider()

    # --- ROW 2: Charts ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Cases by Status")
        # Count how many cases are in each status
        status_counts = cases["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig = px.pie(status_counts, names="Status", values="Count",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Recovery by Industry")
        # Which industries have the most recovered amount?
        industry_data = cases.groupby("industry")["amount_recovered"].sum().reset_index()
        industry_data.columns = ["Industry", "Recovered"]
        fig2 = px.bar(industry_data, x="Industry", y="Recovered",
                      color="Recovered",
                      color_continuous_scale="Greens")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- ROW 3: Cases Table ---
    st.subheader("📋 All Cases")
    # Color-code priority so it's easy to scan
    st.dataframe(cases, use_container_width=True)