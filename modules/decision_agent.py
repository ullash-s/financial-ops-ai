import streamlit as st
import pandas as pd
from datetime import datetime

def analyze_case(row):
    """
    Takes a single case row and returns a recommended action.
    
    This is the core of the decision agent.
    Rule-based now — but the logic could be replaced by an LLM call later.
    """
    
    amount_owed      = row["amount_owed"]
    amount_recovered = row["amount_recovered"]
    status           = row["status"]
    priority         = row["priority"]
    date_opened      = pd.to_datetime(row["date_opened"])
    days_open        = (datetime.now() - date_opened).days

    # Calculate recovery percentage
    recovery_pct = (amount_recovered / amount_owed * 100) if amount_owed > 0 else 0

    # --- Decision Rules (ordered by urgency) ---
    if amount_owed > 20000 and status == "Open":
        action   = "🚨 Escalate Immediately"
        reason   = f"High-value case (${amount_owed:,.0f}) has not been started."
        urgency  = "Critical"

    elif days_open > 60 and status != "Resolved":
        action   = "📬 Send Final Notice"
        reason   = f"Case has been open for {days_open} days without resolution."
        urgency  = "High"

    elif recovery_pct >= 80 and status != "Resolved":
        action   = "✅ Close Case"
        reason   = f"{recovery_pct:.0f}% recovered (${amount_recovered:,.0f}). Ready to close."
        urgency  = "Low"

    elif priority == "High" and status == "Open":
        action   = "📞 Schedule Call"
        reason   = f"High priority case still open. Immediate follow-up needed."
        urgency  = "High"

    elif status == "Resolved":
        action   = "📁 Archive Case"
        reason   = "Case fully resolved. Move to archive."
        urgency  = "None"

    else:
        action   = "👁️ Monitor"
        reason   = f"Case progressing normally. {recovery_pct:.0f}% recovered so far."
        urgency  = "Low"

    return {
        "Recommended Action": action,
        "Reason":             reason,
        "Urgency":            urgency,
        "Days Open":          days_open,
        "Recovery %":         f"{recovery_pct:.0f}%"
    }


def show_decision_agent():
    st.header("🤖 AI Decision Agent")
    st.markdown("Analyzes each case and recommends the next best action.")

    # Load cases
    try:
        cases = pd.read_csv("data/cases.csv")
    except FileNotFoundError:
        st.error("Cases data not found.")
        return

    # --- Section 1: Full Case Analysis ---
    st.subheader("📋 Case Recommendations")

    # Run the agent on every case
    results = []
    for _, row in cases.iterrows():
        analysis = analyze_case(row)
        results.append({
            "Case ID":    row["case_id"],
            "Client":     row["client_name"],
            "Amount":     f"${row['amount_owed']:,.0f}",
            "Status":     row["status"],
            "Action":     analysis["Recommended Action"],
            "Urgency":    analysis["Urgency"],
            "Reason":     analysis["Reason"],
            "Days Open":  analysis["Days Open"],
            "Recovery %": analysis["Recovery %"]
        })

    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)

    st.divider()

    # --- Section 2: Single Case Deep Dive ---
    st.subheader("🔍 Analyze a Single Case")

    case_ids = cases["case_id"].tolist()
    selected = st.selectbox("Select a case to analyze", case_ids)

    if st.button("🤖 Run Analysis"):
        case_row = cases[cases["case_id"] == selected].iloc[0]
        result   = analyze_case(case_row)

        st.markdown(f"### {result['Recommended Action']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Urgency",     result["Urgency"])
        col2.metric("Days Open",   result["Days Open"])
        col3.metric("Recovery %",  result["Recovery %"])

        st.info(f"**Reasoning:** {result['Reason']}")

        st.markdown("**Case Details:**")
        st.json(case_row.to_dict())