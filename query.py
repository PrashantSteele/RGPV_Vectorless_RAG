import json
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# Set up your model - using the Cohere model we set up earlier
MODEL_NAME = "cohere/command-r-plus-08-2024"

def query_document(pdf_path, json_path, question):
    # 1. Load the Tree Structure JSON
    print("Loading document structure...")
    with open(json_path, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    structure_str = json.dumps(structure, indent=2)
    
    # 2. Ask LLM to reason over the structure and select pages
    print("Agent is reasoning over the document structure to find relevant pages...")
    reasoning_prompt = f"""
    You are an expert document retrieval agent.
    Here is the structural 'Table of Contents' of a document:
    {structure_str}
    
    Based on this structure, which page ranges are most likely to contain the answer to the following question?
    Question wuth the clause if found: {question}
    
    Return ONLY a comma-separated list of page numbers to read (e.g. "12, 13, 15"). Do not return any other text.
    """
    
    response = completion(model=MODEL_NAME, messages=[{"role": "user", "content": reasoning_prompt}])
    pages_to_read_str = response.choices[0].message.content.strip()
    print(f"Agent selected pages: {pages_to_read_str}")
    
    # Extract page numbers safely
    pages_to_read = []
    import re
    for num in re.findall(r'\d+', pages_to_read_str):
        pages_to_read.append(int(num))
        
    if not pages_to_read:
        print("Could not identify any relevant pages.")
        return
        
    # 3. Extract text from the selected pages of the PDF
    print("Extracting text from selected pages...")
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page_num in pages_to_read:
        # PyMuPDF pages are 0-indexed, human pages are 1-indexed
        if 0 <= page_num - 1 < len(doc):
            extracted_text += f"\n--- Page {page_num} ---\n"
            extracted_text += doc[page_num - 1].get_text()
            
    # 4. Ask the LLM to answer the question using the extracted text
    print("Generating final answer...")
    answer_prompt = f"""
    You are a helpful assistant. Use the following excerpts from a document to answer the question.
    
    Document Excerpts:
    {extracted_text}
    
    Question: {question}
    """
    
    final_response = completion(model=MODEL_NAME, messages=[{"role": "user", "content": answer_prompt}])
    print("\n" + "="*50)
    print("FINAL ANSWER:")
    print("="*50)
    print(final_response.choices[0].message.content)

if __name__ == "__main__":
    pdf_file = r"Pdf/Ordinance_11PhD.pdf"
    json_file = r"results/Ordinance_11PhD_structure.json"
    
    # Try asking a question!
    user_question = input("What is your question about the PhD Ordinance?: ")
    query_document(pdf_file, json_file, user_question)
