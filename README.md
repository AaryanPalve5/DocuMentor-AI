# 📘Documentor AI 

## 🔷 Overview

This project is an **AI-powered intelligent assistant** that:

* Ingests multimodal content (PDF, Word, Excel, Text, Image, Audio/Video)
* Summarizes & stores insights using vector databases
* Enables interactive chatbot queries with memory
* Includes planning and analytics

---

## 🧩 Project Modules

| File Name         | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `main.py`         | Entry point – launches FastAPI backend and integrates components   |
| `chat_agent.py`   | Defines memory-aware chatbot logic using LangChain-like framework  |
| `config.py`       | Contains all configuration settings (paths, constants, API keys)   |
| `dashboard.py`    | Backend logic for dashboard-related data & analytics               |
| `ingestion.py`    | Handles content ingestion (files, images, audio, video)            |
| `memory_store.py` | Manages vector database and document memory storage                |
| `planner.py`      | Implements planning/agentic logic to generate structured responses |
| `utils.py`        | Common utilities for file conversion, parsing, etc.                |

---

## 🖼️ System Architecture


![Documentor AI Architecture](https://raw.githubusercontent.com/1543siddhant/DocuMentor-AI/main/Documentor%20AI%20architecture.jpg)

---

## ⚙️ Implementation Details

### 1. **Ingestion Module (`ingestion.py`)**

* Accepts PDF, Word, Excel, Images, Videos, Audio
* Uses `PyMuPDF`, `python-docx`, `pandas`, `pytesseract`, and `whisper`
* Converts inputs to raw text
* Sends text to `memory_store.py` for vectorization

### 2. **Memory Store (`memory_store.py`)**

* Uses `FAISS` or `ChromaDB` for vector embedding
* Converts text to embeddings using `SentenceTransformers` or Gemini/OpenAI APIs
* Enables fast similarity search for Q\&A

### 3. **Chat Agent (`chat_agent.py`)**

* Uses LangChain or custom retrieval QA
* Retrieves relevant documents from memory
* Sends queries to LLM (OpenAI/Gemini)
* Maintains short-term memory (last few interactions)

### 4. **Dashboard (`dashboard.py`)**

* Tracks ingestion volume, file types, queries
* Shows usage and chat analytics
* Could be extended with `Plotly`, `Dash`, or a React frontend

### 5. **Planner (`planner.py`)**

* Acts as an intelligent agent layer
* Breaks complex queries into subtasks
* Coordinates with vector store and external tools (optionally)

---

## 🧪 Use Cases

| Use Case                        | Description                                                 |
| ------------------------------- | ----------------------------------------------------------- |
| **Corporate Knowledge Agent**   | Ingest internal docs, summarize SOPs, and answer queries    |
| **Student Study Assistant**     | Accepts notes, textbooks, lectures (video/audio)            |
| **Research Companion**          | Ingest papers, generate insights, track citations           |
| **Enterprise Helpdesk Agent**   | Trained on user manuals, policies, FAQ documents            |
| **Compliance Document Auditor** | Identify red flags, summarize sections across PDF contracts |

---

## 🛠️ Tech Stack

| Layer         | Technologies                                        |
| ------------- | --------------------------------------------------- |
| **Backend**   | Python, FastAPI                                     |
| **AI/ML**     | OpenAI API / Gemini, FAISS / ChromaDB, LangChain    |
| **NLP**       | SentenceTransformers, Tesseract, Whisper            |
| **Ingestion** | PyMuPDF, python-docx, pandas, pytesseract, moviepy  |
| **Storage**   | Local/Cloud file system, Vector DB (FAISS/ChromaDB) |
| **Dashboard** | Matplotlib, Plotly                                  |

---
