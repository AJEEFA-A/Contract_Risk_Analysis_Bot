import streamlit as st
import pdfplumber
from groq import Groq
from fpdf import FPDF
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ------------------ PDF READER FUNCTION ------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# ------------------ PDF REPORT GENERATOR ------------------
def generate_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)

    for line in report_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_name = "legal_risk_report.pdf"
    pdf.output(file_name)
    return file_name

# ------------------ UI HEADER ------------------
st.title("AI Contract Risk Assistant 🧠⚖️")
st.write("Upload a contract to analyze risks, get simple explanation, and safer version.")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])

# ------------------ MAIN LOGIC ------------------
if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("📄 Contract Text")
    st.text_area("Extracted Text", text, height=250)

    # ------------------ AI ANALYSIS WITH NORMALIZATION ------------------
    prompt = f"""
You are a legal risk assessment system.

Step 1: If the contract is in Hindi, first translate it to English internally.
Step 2: Then perform all legal analysis on the English version.

From the contract, explicitly identify and list:
- Penalty clauses
- Indemnity clauses
- Unilateral termination clauses
- Arbitration & jurisdiction clauses
- Auto-renewal / lock-in clauses
- Non-compete / IP transfer clauses

For each, give:
Clause type:
Risk level (Low/Medium/High):
Reason:

Also give a simple overall summary at the end.

Contract:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    analysis = response.choices[0].message.content

    st.subheader("🤖 AI Legal Risk Analysis")
    st.write(analysis)

    # ------------------ RISK HEATMAP ------------------
    st.subheader("🔥 Risk Heatmap")
    lines = analysis.split("\n")

    for line in lines:
        if "High" in line:
            st.error(line)
        elif "Medium" in line:
            st.warning(line)
        elif "Low" in line:
            st.success(line)

    # ------------------ SIMPLE / TAMIL MODE ------------------
    mode = st.selectbox("Explanation Mode", ["Legal English", "Simple English", "Tamil"])

    prompt_lang = f"""
First, translate the contract to English if it is in Hindi or any other language.
Then explain the contract in {mode} for a small business owner in clear and simple terms.

Contract:
{text}
"""
    response_lang = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt_lang}]
    )

    explanation = response_lang.choices[0].message.content

    st.subheader("🗣️ Explanation")
    st.write(explanation)

    # ------------------ NEGOTIATION MODE ------------------
    if st.button("🛡️ Generate Safer Contract (Negotiation Mode)"):
        prompt2 = f"""
First, translate the contract into English if it is in Hindi or any other language.
Then rewrite the contract in a safer, fair version for SMEs in English.
Remove one-sided clauses and risky terms.

Contract:
{text}
"""


        response2 = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt2}]
        )

        safer = response2.choices[0].message.content

        st.subheader("✍️ Safer Negotiated Contract")
        st.write(safer)

    # ------------------ PDF EXPORT FOR LEGAL REVIEW ------------------
    if st.button("📥 Download Legal Report (PDF)"):
        full_report = f"""
AI CONTRACT RISK REPORT

========================
RISK ANALYSIS (English)
========================
{analysis}

========================
BUSINESS SUMMARY (English)
========================
This report is generated in English for legal review and documentation purposes.

"""

        pdf_file = generate_pdf(full_report)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="legal_risk_report.pdf",
                mime="application/pdf"
            )

