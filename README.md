# 🚀 RGPV Self-Hosted PageIndex RAG

A lightweight, self-hosted Retrieval-Augmented Generation (RAG) application built with Streamlit and PageIndex. Unlike traditional RAG architectures that require vector embeddings and vector databases, this solution uses PageIndex's document indexing and retrieval capabilities for faster deployment, lower infrastructure costs, and simplified maintenance.

## 📖 Overview

This application enables users to interact with institutional documents, ordinances, regulations, manuals, and knowledge bases using natural language queries.
The system retrieves relevant document sections directly from indexed pages and provides AI-generated responses grounded in the source documents.

## ✨ Key Features

* 📄 PDF Document Processing
* 🔍 Page-Level Intelligent Retrieval
* 🤖 AI-Powered Question Answering
* 🚫 No Vector Database Required
* 🏠 Fully Self-Hosted Architecture



## 🏗 Architecture

```text
User Query
    │
    ▼
Streamlit Interface
    │
    ▼
PageIndex Retrieval Engine
    │
    ▼
Relevant Document Pages
    │
    ▼
LLM (Cohere)
    │
    ▼
Grounded Response
```

---

## 🔄 Traditional RAG vs PageIndex RAG

| Feature                   | Traditional RAG | Self-Hosted PageIndex |
| ------------------------- | --------------- | --------------------- |
| Embeddings Required       | ✅ Yes           | ❌ No                  |
| Vector Database           | ✅ Required      | ❌ Not Required        |
| Embedding Generation Cost | High            | None                  |
| Infrastructure Complexity | High            | Low                   |
| Setup Time                | Moderate        | Fast                  |
| Storage Requirements      | High            | Low                   |
| Document Reindexing       | Costly          | Simple                |
| Self Hosting              | Possible        | Native                |
| Maintenance               | High            | Minimal               |


## ⚙️ Installation

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

## 📋 Requirements

```text
streamlit
pageindex
cohere
python-dotenv
pandas
pypdf
```

---

## 💡 Example Queries

* What are the eligibility requirements for PhD admission?
* Explain Ordinance 11 in simple language.
* What is the procedure for synopsis submission?
* How many publications are required before thesis submission?
* What are the responsibilities of a PhD supervisor?

---

## 🔒 Privacy & Security

* Documents remain on your infrastructure.
* No external vector database required.
* Suitable for universities, enterprises, and institutional knowledge bases.
* Supports completely self-hosted deployment.

---

## 🎯 Use Cases

### Higher Education

* University Ordinance Chatbots
* Student Information Systems
* Academic Regulation Assistants

### Enterprises

* HR Policy Assistants
* SOP Knowledge Systems
* Internal Documentation Search

### Research

* Thesis Regulations
* Research Guidelines
* Institutional Repositories

---

## 🚀 Future Enhancements

* Multi-document retrieval
* Hybrid search
* User authentication
* Conversation memory
* Citation highlighting
* Multi-language support

---

## 👨‍💻 Developed By

**Prashant Steele**

Research Scholar, Mechanical Engineering

University Institute of Technology (UIT)

Rajiv Gandhi Proudyogiki Vishwavidyalaya (RGPV), Bhopal

Research Interests:

* Predictive Maintenance
* Agentic AI
* Retrieval-Augmented Generation (RAG)
* Multivariate Time Series Forecasting
* Industrial AI Applications

---

## 📜 License

This project is released under the MIT License.
