import streamlit as st
import pandas as pd
import json
import os
import base64
import pdfplumber
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image_to_base64(file):
    """Convert uploaded image to base64 for API transmission."""
    return base64.b64encode(file.read()).decode("utf-8")


def extract_text_from_pdf(file):
    """Extract raw text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_with_ai_text(text):
    """Extract invoice fields from plain text or PDF text."""
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
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def extract_with_ai_image(image_file):
    """
    Send image directly to Groq vision model.
    No OCR needed — AI reads the image like a human would.
    """
    # Reset file pointer and encode
    image_file.seek(0)
    image_data = encode_image_to_base64(image_file)
    
    # Detect media type
    file_type = image_file.type
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # Groq vision model
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{file_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": """You are an invoice processing assistant.
Extract the following fields from this invoice image.

Return ONLY a valid JSON object with these exact keys:
- invoice_number
- client_name
- invoice_date
- due_date
- total_amount
- payment_status

If a field is not found, use "Not Found" as the value.
Do not include any explanation or markdown — just the raw JSON."""
                    }
                ]
            }
        ],
        temperature=0.1
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def show_invoice_processor():
    st.header("🧾 Invoice Processing System")
    st.markdown("Upload a **PDF, image, or text** invoice — AI extracts key fields automatically.")

    tab1, tab2 = st.tabs(["📁 Upload Invoice", "🧪 Try Sample Invoice"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Upload invoice file",
            type=["txt", "pdf", "png", "jpg", "jpeg"]
        )

        if uploaded_file:
            file_type = uploaded_file.type

            if file_type == "application/pdf":
                st.info("📄 PDF detected — extracting text...")
                with st.spinner("Reading PDF..."):
                    text = extract_text_from_pdf(uploaded_file)
                with st.expander("📄 View Extracted Text"):
                    st.text(text)
                if text:
                    process_and_display_text(text)
                else:
                    st.error("Could not extract text from PDF.")

            elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
                st.info("🖼️ Image detected — sending to AI vision model...")
                st.image(uploaded_file, caption="Uploaded Invoice", width=400)
                process_and_display_image(uploaded_file)

            else:
                text = uploaded_file.read().decode("utf-8")
                st.info("📝 Text file detected...")
                process_and_display_text(text)

    with tab2:
        try:
            with open("assets/sample_invoice.txt", "r") as f:
                sample_text = f.read()
            st.text_area("Sample Invoice Text", sample_text, height=300)
            if st.button("🤖 Extract with AI"):
                process_and_display_text(sample_text)
        except FileNotFoundError:
            st.error("Sample invoice file not found.")


def process_and_display_text(text):
    """Handle text/PDF invoices."""
    with st.spinner("🤖 AI is reading the invoice..."):
        try:
            fields = extract_with_ai_text(text)
        except Exception as e:
            st.error(f"AI extraction failed: {e}")
            return
    display_results(fields)


def process_and_display_image(image_file):
    """Handle image invoices via vision model."""
    with st.spinner("🤖 AI vision model is reading the invoice image..."):
        try:
            fields = extract_with_ai_image(image_file)
        except Exception as e:
            st.error(f"AI vision extraction failed: {e}")
            return
    display_results(fields)


def display_results(fields):
    """Shared display function for all invoice types."""
    st.success("✅ AI extraction complete!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Client",       fields.get("client_name",    "Not Found"))
    col2.metric("Total Amount", fields.get("total_amount",   "Not Found"))
    col3.metric("Status",       fields.get("payment_status", "Not Found"))

    st.divider()

    st.subheader("📋 All Extracted Fields")
    df = pd.DataFrame(fields.items(), columns=["Field", "Value"])
    st.dataframe(df, use_container_width=True)

    with st.expander("🔍 View Raw AI Response"):
        st.json(fields)