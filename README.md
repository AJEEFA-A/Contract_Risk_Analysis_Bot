# AI Contract Risk Analysis Bot

## Problem Statement
Build a GenAI-powered legal assistant that helps SMEs understand contracts, identify risks, and receive actionable insights in simple language.

## Project Description
This project is an AI-powered Contract Analysis and Risk Assessment Assistant designed for small and medium businesses. The system analyzes legal contracts, identifies risky clauses, and provides simplified explanations for non-legal users.

The system supports multilingual contracts. If a contract is uploaded in Hindi, it is internally translated into English for consistent NLP analysis.

## Features
- Contract risk detection (Penalty, Indemnity, Termination, Arbitration clauses)
- Multilingual handling (Hindi → English normalization)
- Simple business explanation
- Negotiation-ready safer contract generation
- Risk heatmap visualization
- PDF export for legal review

## Tech Stack
- Python
- Streamlit
- Groq LLM API
- pdfplumber
- FPDF

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
