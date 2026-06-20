# RGPV_VL_Rag

A simple, local implementation of **PageIndex** — a Vectorless, Reasoning-based RAG system.

## PageIndex Vectorless RAG vs. Traditional RAG

**Traditional RAG** relies on **Vector Databases**. It breaks documents into artificial chunks and uses semantic similarity to find information. 
* **The Problem:** Similarity is not the same as relevance. Traditional RAG often misses the bigger picture, lacks multi-step reasoning, and acts like a "black box" making it hard to trace why certain text was retrieved.

**PageIndex Vectorless RAG** uses a **Hierarchical Tree Index** instead of vectors. It organizes a document into its natural sections (like a Table of Contents) and uses an LLM to actively reason and search through the tree.
* **The Solution:** No chunking and no vector databases. It provides context-aware, human-like reasoning to find exactly what you need. It is fully traceable, explainable, and far more accurate for complex, professional documents.

## Key Features
- **No Vector DB:** Uses document structure and LLM reasoning for retrieval.
- **No Chunking:** Keeps natural document sections and hierarchy intact.
- **Traceable & Explainable:** You can see exactly how the LLM reasoned to find the answer.
- **Highly Accurate:** Excellent for professional documents that demand domain expertise.

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key_here
```

### 3. Run the application
Use the provided batch script or run the Python app directly:
```bash
./run_app.bat
# Or
python app.py
```
