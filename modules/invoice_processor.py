import streamlit as st
import re
import pandas as pd

def extract_invoice_fields(text):
    def find(pattern, text, default="Not Found"):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    invoice_number = find(r"Invoice Number[:\s]+([A-Z0-9\-]+)", text)
    invoice_date   = find(r"Date[:\s]+([\w]+ \d{1,2},? \d{4})", text)
    due_date       = find(r"Due Date[:\s]+([\w]+ \d{1,2},? \d{4})", text)
    client_name    = find(r"Bill To:\s*\n\s*(.+)", text)
    total_amount   = find(r"Total Amount Due[:\s]+\$?([\d,]+\.?\d*)", text)
    payment_status = find(r"Payment Status[:\s]+(\w+)", text)

    return {
        "Invoice Number": invoice_number,
        "Client Name":    client_name,
        "Invoice Date":   invoice_date,
        "Due Date":       due_date,
        "Total Amount":   f"${total_amount}" if total_amount != "Not Found" else "Not Found",
        "Payment Status": payment_status,
    }


def show_invoice_processor():
    st.header("🧾 Invoice Processing System")
    st.markdown("Upload a plain text invoice to extract structured data automatically.")

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

            if st.button("⚙️ Extract Invoice Data"):
                process_and_display(sample_text)
        except FileNotFoundError:
            st.error("Sample invoice file not found.")


def process_and_display(text):
    with st.spinner("Extracting invoice fields..."):
        fields = extract_invoice_fields(text)

    st.success("✅ Extraction complete!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Client", fields["Client Name"])
    col2.metric("Total Amount", fields["Total Amount"])
    col3.metric("Status", fields["Payment Status"])

    st.divider()

    st.subheader("📋 All Extracted Fields")
    df = pd.DataFrame(fields.items(), columns=["Field", "Value"])
    st.dataframe(df, use_container_width=True)