import streamlit as st
import json
import fitz  # PyMuPDF
import re
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()

MODEL_NAME = "cohere/command-r-plus-08-2024"
PDF_FILE = r"Pdf\Ordinance_11PhD.pdf"
JSON_FILE = r"results\Ordinance_11PhD_structure.json"

st.set_page_config(page_title="AI Assistant - RGPV", page_icon="🎓", layout="centered")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown('<p class="main-header">AI Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ordinance 11(PhD) | Year 2019 onwards</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.1rem; color: #1E3A8A; font-weight: 600; margin-top: 1px; margin-bottom: 0px;">राजीव गांधी प्रौद्योगिकी विश्वविद्यालय, भोपाल<br>(मध्य प्रदेश का राज्य तकनीकी विश्वविद्यालय)</p>', unsafe_allow_html=True)
    

# Sidebar
with st.sidebar:
    st.image("logo.png", width=150)
    st.title("About")
    st.write("This AI Assistant uses **Reasoning-based RAG** to answer your questions accurately about the RGPV PhD Ordinance.")
    st.divider()
    st.markdown("<div style='font-size: 0.8rem; color: gray; line-height: 1.4;'><b>Designed By :</b><br>Prashant Steele<br>Research Scholar (ME)</div>", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming message
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am your AI Assistant for the RGPV PhD Ordinance. What would you like to know?"})

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about the PhD Ordinance..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        try:
            # 1. Load the Tree Structure JSON
            with st.status("Analyzing document structure...", expanded=True) as status:
                with open(JSON_FILE, 'r', encoding='utf-8') as f:
                    structure = json.load(f)
                structure_str = json.dumps(structure, indent=2)
                
                status.update(label="Reasoning over document outline...", state="running")
                
                # 2. Ask LLM to reason over the structure
                reasoning_prompt = f"""
                You are an expert document retrieval agent.
                Here is the structural 'Table of Contents' of a document:
                {structure_str}
                
                Based on this structure, which page ranges are most likely to contain the answer to the following question?
                Question: {prompt}
                
                Return ONLY a comma-separated list of page numbers to read (e.g. "12, 13, 15"). Do not return any other text.
                """
                
                response = completion(model=MODEL_NAME, messages=[{"role": "user", "content": reasoning_prompt}])
                pages_to_read_str = response.choices[0].message.content.strip()
                
                # Extract page numbers safely
                pages_to_read = []
                for num in re.findall(r'\d+', pages_to_read_str):
                    pages_to_read.append(int(num))
                
                if not pages_to_read:
                    status.update(label="Analysis complete.", state="complete", expanded=False)
                    st.write("I could not identify any relevant pages for that question based on the document's structure. Please try rephrasing.")
                    st.session_state.messages.append({"role": "assistant", "content": "I could not identify any relevant pages for that question based on the document's structure."})
                    st.stop()
                
                st.write(f"🧠 AI identified relevant pages: {pages_to_read}")
                
                # 3. Extract text from the selected pages of the PDF
                status.update(label=f"Extracting text from pages {pages_to_read}...", state="running")
                doc = fitz.open(PDF_FILE)
                extracted_text = ""
                for page_num in pages_to_read:
                    # PyMuPDF pages are 0-indexed
                    if 0 <= page_num - 1 < len(doc):
                        extracted_text += f"\n--- Page {page_num} ---\n"
                        extracted_text += doc[page_num - 1].get_text()
                
                status.update(label="Generating final answer...", state="running")
                
                # 4. Ask the LLM to answer the question using the extracted text
                # We also include previous chat history for context
                messages = []
                for msg in st.session_state.messages[:-1]: # exclude the current prompt since we add it below
                    messages.append({"role": msg["role"], "content": msg["content"]})
                    
                answer_prompt = f"""
                You are the RGPV Bhopal AI Assistant. Use the following excerpts from the Ordinance 11 (PhD) document to accurately answer the user's question.
                If the answer is not contained in the excerpts, politely state that you don't know based on the Ordinance.
                
                Document Excerpts:
                {extracted_text}
                
                Question: {prompt}
                """
                messages.append({"role": "user", "content": answer_prompt})
                
                final_response = completion(model=MODEL_NAME, messages=messages)
                final_answer = final_response.choices[0].message.content
                
                status.update(label="Complete!", state="complete", expanded=False)
            
            # Display final answer
            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
