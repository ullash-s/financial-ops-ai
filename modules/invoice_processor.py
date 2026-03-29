import streamlit as st
import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_with_ai(text):
    """
    Uses Groq (Llama 3) to extract invoice fields from unstructured text.
    This is real AI — send raw text, get structured data back.
    No hardcoded patterns. Works on any invoice format.
    """

    prompt = f"""
    You are an invoice processing assistant.
    Extract the following fields from the invoice text below.
    
    Return ONLY a valid JSON object with these exact keys:
    - invoice_number
    - client_name
    - invoice_date
    - due_date
    - total_amount
    - payment_status
    
    If a field is not found, use "Not Found" as the value.
    Do not include any explanation or markdown — just the raw JSON.
    
    Invoice Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Free, fast Llama 3 model on Groq
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1   # Low temperature = more consistent, predictable output
    )

    raw = response.choices[0].message.content.strip()
    # Remove markdown code blocks if model adds them
    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)


def show_invoice_processor():
    st.header("🧾 Invoice Processing System")
    st.markdown("Upload a plain text invoice — AI extracts the key fields automatically.")

    tab1, tab2 = st.tabs(["📁 Upload Invoice", "🧪 Try Sample Invoice"])

    with tab1:
        uploaded_file = st.file_uploader("Upload a .txt invoice file", type=["txt"])
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            process_and_display(text)

    with tab2:
        try:
            with open("assets/sample_invoice.txt", "r") as f:
                sample_text = f.read()

            st.text_area("Sample Invoice Text", sample_text, height=300)

            if st.button("🤖 Extract with AI"):
                process_and_display(sample_text)

        except FileNotFoundError:
            st.error("Sample invoice file not found.")


def process_and_display(text):
    """Send text to Groq and display extracted fields."""

    with st.spinner("🤖 AI is reading the invoice..."):
        try:
            fields = extract_with_ai(text)
        except Exception as e:
            st.error(f"AI extraction failed: {e}")
            return

    st.success("✅ AI extraction complete!")

    # Show key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Client",       fields.get("client_name",    "Not Found"))
    col2.metric("Total Amount", fields.get("total_amount",   "Not Found"))
    col3.metric("Status",       fields.get("payment_status", "Not Found"))

    st.divider()

    # Show all fields in a clean table
    st.subheader("📋 All Extracted Fields")
    df = pd.DataFrame(fields.items(), columns=["Field", "Value"])
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Show raw AI response for transparency
    with st.expander("🔍 View Raw AI Response"):
        st.json(fields)