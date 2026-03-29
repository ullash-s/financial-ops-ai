import streamlit as st
import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATA_PATH = "data/cases.csv"

def load_cases():
    return pd.read_csv(DATA_PATH)

def save_cases(df):
    df.to_csv(DATA_PATH, index=False)

def get_ai_action(user_message, df):
    """
    Send user message + current data to AI.
    AI returns a structured JSON action to execute.
    This is the core of the conversational data interface.
    """
    # Give AI full context of current data
    cases_summary = df.to_string(index=False)

    system_prompt = f"""
You are a data operations assistant for a financial asset recovery company.
You help users manage their cases table through natural language.

CURRENT CASES DATA:
{cases_summary}

VALID FIELDS:
- case_id (format: C001, C002, etc.)
- client_name (string)
- amount_owed (number)
- amount_recovered (number)
- status (Open, In Progress, Resolved)
- priority (High, Medium, Low)
- assigned_agent (string)
- date_opened (YYYY-MM-DD)
- industry (string)

You must respond with ONLY a valid JSON object — no explanation, no markdown.

For CREATE action:
{{"action": "create", "data": {{"case_id": "C016", "client_name": "...", "amount_owed": 0, "amount_recovered": 0, "status": "Open", "priority": "Medium", "assigned_agent": "...", "date_opened": "2024-01-01", "industry": "..."}}}}

For UPDATE action:
{{"action": "update", "case_id": "C001", "field": "status", "value": "Resolved"}}

For DELETE action:
{{"action": "delete", "case_id": "C001"}}

For QUERY action:
{{"action": "query", "response": "Your answer in plain English here"}}

For unclear requests:
{{"action": "clarify", "response": "What you need clarified"}}

Rules:
- For CREATE: auto-generate the next case_id based on existing ones
- For missing fields in CREATE: use sensible defaults
- For QUERY: answer directly from the data provided
- Always return valid JSON only
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def execute_action(action_obj, df):
    """
    Execute the AI's recommended action on the DataFrame.
    Returns (updated_df, success_message, error_message)
    """
    action = action_obj.get("action")

    if action == "create":
        new_row = action_obj.get("data", {})
        # Auto-generate case_id if not provided correctly
        existing_ids = df["case_id"].tolist()
        max_num = max([int(id[1:]) for id in existing_ids if id[1:].isdigit()])
        new_row["case_id"] = f"C{str(max_num + 1).zfill(3)}"
        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_cases(new_df)
        return new_df, f"✅ Created new case **{new_row['case_id']}** for **{new_row.get('client_name', 'Unknown')}**", None

    elif action == "update":
        case_id = action_obj.get("case_id")
        field   = action_obj.get("field")
        value   = action_obj.get("value")

        if case_id not in df["case_id"].values:
            return df, None, f"❌ Case {case_id} not found."

        df.loc[df["case_id"] == case_id, field] = value
        save_cases(df)
        return df, f"✅ Updated **{case_id}** — set **{field}** to **{value}**", None

    elif action == "delete":
        case_id = action_obj.get("case_id")
        if case_id not in df["case_id"].values:
            return df, None, f"❌ Case {case_id} not found."
        df = df[df["case_id"] != case_id].reset_index(drop=True)
        save_cases(df)
        return df, f"✅ Deleted case **{case_id}**", None

    elif action in ["query", "clarify"]:
        return df, action_obj.get("response", "Here is the information you requested."), None

    else:
        return df, None, "❌ I didn't understand that request. Please try again."


def show_chat():
    """Floating chat UI rendered at the bottom of every page."""

    st.markdown("---")
    st.markdown("### 💬 AI Operations Assistant")
    st.markdown("Ask me to create, update, delete, or query cases in plain English.")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("e.g. Create a new case for Tesla Inc, $45,000, High priority")

    if user_input:
        # Show user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response and execute
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    df = load_cases()
                    action_obj = get_ai_action(user_input, df)
                    df, success, error = execute_action(action_obj, df)

                    if success:
                        st.markdown(success)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": success
                        })
                    if error:
                        st.markdown(error)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error
                        })

                except Exception as e:
                    msg = f"❌ Something went wrong: {e}"
                    st.markdown(msg)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": msg
                    })

        st.rerun()