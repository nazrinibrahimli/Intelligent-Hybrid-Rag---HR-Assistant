import streamlit as st
import pandas as pd
import pypdf
import re
import ollama

# --- SET UP THE PAGE ---
st.set_page_config(page_title="Expat Legal HR Bot", page_icon="⚖️", layout="wide")
st.title("⚖️ Expat Legal HR Assistant")
st.markdown("### Intelligent Hybrid RAG: Structured Data + Local LLM Reasoning")
st.write("---")

# --- DATA: THE SOURCE OF TRUTH (Page 15) ---
pto_data = {
    'Hired': ['Post-Nov-23']*3 + ['Pre-Nov-23']*3,
    'Tenure': ['0-2yrs', '2-5yrs', '5+yrs', '0-2yrs', '2-5yrs', '5+yrs'],
    'Accrual_Hrs': [6, 7, 8, 6.77, 8, 10],
    'Max_Year_Days': [11, 15, 20, 11, 15, 20],
    'Max_Carryover_Days': [10, 12, 15, 10, 12, 15]
}
df_pto = pd.DataFrame(pto_data)

# --- 1. THE RETRIEVAL (Finding the PDF Page) ---
def get_pdf_context(search_term):
    try:
        reader = pypdf.PdfReader("./data/handbook.pdf") 
        pages_found = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if search_term.lower() in text.lower():
                pages_found.append((i + 1, text))
        return pages_found
    except Exception as e:
        return [(-1, f"Error reading PDF: {e}")]

# --- 2. THE REASONING (Sending Page to Ollama) ---
def generate_ai_reasoning(user_question, pdf_context):
    prompt = f"""
    You are an expert HR assistant. Read the following messy, bilingual handbook text. 
    Ignore the Spanish translation. Use step-by-step reasoning to extract a short, 
    plain-English answer to the user's question.

    User Question: {user_question}
    Handbook Context: {pdf_context}

    Answer:
    """
    try:
        response = ollama.chat(model='llama3:8b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']
    except Exception as e:
        return f"AI Generation failed. Make sure 'ollama run llama3:8b' is running in another terminal. Error: {e}"

# --- 3. THE INTERFACE & ROUTING ---
query = st.text_input("Ask a question about HR policy or PTO:", placeholder="e.g., What are the notice days of employment?")

if query:
    clean_query = re.sub(r'[^\w\s]', '', query).lower()
    words = clean_query.split()
    
    # PATH A: Table Routing
    if any(word in clean_query for word in ['how many', 'accrual', 'table', 'limit', 'pto', 'sick']):
        st.success("Fetched from Verified PTO Database")
        if 'sick' in clean_query:
            st.info("Note: Centro uses PTO for sick leave. There is no separate sick bank (Ref: Page 15).")
        st.table(df_pto)
    
    # PATH B: RAG + Reasoning Routing
    else:
        st.warning("Retrieving handbook page and applying AI reasoning. This may take a few seconds...")
        
        priority_words = ['notice', 'harassment', 'resignation', 'integrity', 'professionalism', 'dress', 'employment']
        search_term = next((pw for pw in priority_words if pw in words), words[-1] if words else "")
        
        if search_term:
            results = get_pdf_context(search_term)
            if results:
                # Grab the first matching page
                page_num, raw_text = results[0]
                clean_context = raw_text.replace('\n', ' ').replace('  ', ' ')
                
                # Send it to Ollama for reasoning
                ai_answer = generate_ai_reasoning(query, clean_context)
                
                # Display the smart answer
                st.subheader("🤖 AI Reasoning Summary")
                st.write(ai_answer)
                
                # Dropdown for the raw, messy text to prove where it came from
                with st.expander(f"🔍 View Raw Source Text (Page {page_num})"):
                    st.markdown(f"*{clean_context}*")
                st.success("Analysis complete.")
            else:
                st.error(f"Could not find information related to '{search_term}'.")
        else:
            st.error("Please enter a question.")