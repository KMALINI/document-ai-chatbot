\# Document-Based AI Chatbot using RAG



A document question-answering chatbot that allows users to upload a PDF and ask questions about its content.



The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the uploaded document and generate answers using a locally running Llama 3.2 model.



\## Features



\- Upload PDF documents

\- Extract text from PDF files

\- Split documents into smaller chunks

\- Generate vector embeddings

\- Store and search document embeddings using FAISS

\- Retrieve relevant document content for each question

\- Generate answers using Llama 3.2

\- Chat-style question and answer interface

\- Ask multiple questions about the same document



\## Technology Stack



\### Frontend

\- React

\- Vite

\- JavaScript

\- HTML

\- CSS



\### Backend

\- Python

\- FastAPI

\- PyPDF

\- LangChain Text Splitters



\### AI / RAG

\- Sentence Transformers

\- all-MiniLM-L6-v2

\- FAISS

\- Ollama

\- Llama 3.2



\## How It Works



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



\## Project Structure



Document-AI-Chatbot/

│

├── backend/

│   ├── main.py

│   ├── requirements.txt

│   └── ...

│

├── frontend/

│   ├── src/

│   ├── public/

│   ├── package.json

│   └── ...

│

├── .gitignore

└── README.md



\## Running the Project Locally



\### Backend



Open PowerShell:



```powershell

cd backend



Activate the virtual environment:



.\\venv\\Scripts\\activate



Start the backend:



uvicorn main:app --reload



Backend runs at:



http://127.0.0.1:8000



Frontend



Open another PowerShell window:



cd frontend

npm install

npm run dev



Frontend runs at:



http://localhost:5173



AI Model



The project currently uses:



Llama 3.2 through Ollama for answer generation

all-MiniLM-L6-v2 for document and question embeddings

FAISS for similarity search



The AI model runs locally, so an external OpenAI API key is not required for the current version.



Current Limitations

Works best with text-based PDF files.

Scanned or image-only PDFs currently require OCR support.

The current version stores the uploaded document during the application session.

Ollama must be installed to run the local Llama 3.2 model.

Future Improvements

OCR support for scanned PDFs

Multiple document support

Persistent vector database

User authentication

Conversation history

Cloud deployment

Hosted LLM integration

Improved document management

Author



Malini K



Computer and Communication Engineering

Sri Sairam Institute of Technology



Project Status



Currently under development.

