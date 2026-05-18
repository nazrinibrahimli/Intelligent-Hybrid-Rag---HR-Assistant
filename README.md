# Intelligent-Hybrid-Rag---HR-Assistant


A privacy-first **Hybrid Retrieval-Augmented Generation (RAG)** application built to handle high-stakes corporate compliance queries. The system processes an unstructured, bilingual (English/Spanish) Employee Handbook alongside a structured payroll/PTO database, using a custom routing layer in Python to ensure 100% precision for data lookups while utilizing a local LLM for text reasoning.

## Key Features
- **Deterministic Routing:** Automatically intercepts numerical, payroll, and PTO inquiries and routes them to structured data tables to eliminate AI hallucinations.
- **Privacy-Preserving Local Brain:** Uses a local instance of **Llama 3 (8B)** managed via **Ollama**, ensuring zero data leakage and 100% private local execution.
- **Bilingual Text Filtering:** Instructs the LLM to filter out parallel Spanish translations and synthesize plain-English compliance rules from unstructured text blocks.
- **Audit-Ready UI:** Built with Streamlit, displaying clean synthesis containers (`st.expander`) that allow users to inspect raw source PDF pages for complete transparency.

## Technical Stack
- **Frontend Framework:** Streamlit
- **Data Engineering:** Pandas, Python Regular Expressions (`re`)
- **Document Parsing:** PyPDF
- **Orchestration Layer:** Local Ollama Engine
- **Core Model:** Llama 3 (8B Parameter Model)

## How to Run This Project Locally
*(Instructions for external developers downloading this repo)*

1. Install and run Ollama with Llama 3:
   ```zsh
   ollama run llama3:8b

2. Activate your virtual environment and install dependencies:
    ```zsh
   source venv/bin/activate
   pip install streamlit pandas pypdf ollama

3. Launch the application front-end
    ```zsh
    streamlit run app.py        
