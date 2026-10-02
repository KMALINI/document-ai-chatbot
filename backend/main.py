from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import shutil
import numpy as np
import ollama


app = FastAPI()


# --------------------------------------------------
# CORS
# Allow React frontend to communicate with FastAPI
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Global document storage
# --------------------------------------------------

faiss_index = None
document_chunks = []


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Document AI Chatbot Backend is Running!"
    }


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    global faiss_index
    global document_chunks

    file_path = "uploaded.pdf"

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # --------------------------------------------------
    # Read PDF
    # --------------------------------------------------

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted_text = page.extract_text() or ""

        text += extracted_text


    # --------------------------------------------------
    # Split document into chunks
    # --------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_text(text)

    document_chunks = chunks


    # --------------------------------------------------
    # Create embeddings
    # --------------------------------------------------

    embeddings = embedding_model.encode(
        chunks
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")


    # --------------------------------------------------
    # Create FAISS index
    # --------------------------------------------------

    dimension = embeddings.shape[1]

    faiss_index = faiss.IndexFlatL2(
        dimension
    )

    faiss_index.add(
        embeddings
    )


    # --------------------------------------------------
    # Return upload information
    # --------------------------------------------------

    return {

        "filename": file.filename,

        "message":
            "PDF processed successfully!",

        "text_length":
            len(text),

        "total_chunks":
            len(chunks),

        "embedding_dimensions":
            dimension,

        "faiss_vectors":
            faiss_index.ntotal
    }


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.post("/ask")
async def ask_question(
    question: str
):

    # --------------------------------------------------
    # Check whether PDF is uploaded
    # --------------------------------------------------

    if faiss_index is None:

        return {

            "error":
                "Please upload a PDF first."
        }


    # --------------------------------------------------
    # Convert question into embedding
    # --------------------------------------------------

    question_embedding = embedding_model.encode(
        [question]
    )

    question_embedding = np.array(
        question_embedding
    ).astype("float32")


    # --------------------------------------------------
    # Retrieve relevant chunks
    #
    # Previously: top 3 chunks
    # Now: top 8 chunks
    # --------------------------------------------------

    number_of_chunks = min(
        8,
        len(document_chunks)
    )

    distances, indices = faiss_index.search(
        question_embedding,
        number_of_chunks
    )


    # --------------------------------------------------
    # Collect retrieved chunks
    # --------------------------------------------------

    relevant_chunks = []

    for index in indices[0]:

        if index >= 0:

            relevant_chunks.append(
                document_chunks[index]
            )


    # --------------------------------------------------
    # Combine retrieved chunks
    # --------------------------------------------------

    context = "\n\n".join(
        relevant_chunks
    )


    # --------------------------------------------------
    # Prompt Llama
    # --------------------------------------------------

    prompt = f"""
You are a document question-answering assistant.

Your job is to answer the user's question using ONLY
the information explicitly available in the document
context provided below.

Important rules:

1. Do not invent information.

2. Do not make assumptions or guesses.

3. Answer directly and clearly.

4. If the question asks about a specific topic,
   concept, component, method, technology, or feature,
   use the relevant information from the context.

5. If the question asks about the overall document,
   identify the main topic or purpose using the context.

6. Do not confuse related concepts with the exact answer.

7. Do not treat tools, technologies, concepts, or
   frameworks as programming languages unless the
   document explicitly describes them as programming
   languages.

8. If the answer cannot be found anywhere in the
   provided context, say exactly:

"I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""


    # --------------------------------------------------
    # Generate answer using Llama 3.2
    # --------------------------------------------------

    response = ollama.chat(

        model="llama3.2",

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]
    )


    answer = response[
        "message"
    ][
        "content"
    ]


    # --------------------------------------------------
    # Return answer
    # --------------------------------------------------

    return {

        "question":
            question,

        "answer":
            answer,

        "relevant_chunks":
            relevant_chunks,

        "distances":
            distances[0].tolist()
    }