# Document-Based AI Chatbot using RAG

A document question-answering chatbot that allows users to upload a PDF and ask questions about its content.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the uploaded document and generate answers using a locally running Llama 3.2 model.

---

## Features

- Upload PDF documents
- Extract text from PDF files
- Split documents into smaller chunks
- Generate vector embeddings
- Store and search document embeddings using FAISS
- Retrieve relevant document content for each question
- Generate answers using Llama 3.2
- Chat-style question and answer interface
- Ask multiple questions about the same document
- Runs locally without requiring an OpenAI API key

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

### Backend

- Python
- FastAPI
- PyPDF
- LangChain Text Splitters

### AI / RAG

- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- Ollama
- Llama 3.2

---

## How It Works

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
Sentence Transformer Embeddings
    ↓
FAISS Vector Search
    ↓
User Question
    ↓
Question Embedding
    ↓
Relevant Document Chunks Retrieved
    ↓
Llama 3.2
    ↓
Answer
