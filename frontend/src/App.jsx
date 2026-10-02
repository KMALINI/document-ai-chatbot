import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadMessage("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadMessage("Please select a PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploadMessage("Uploading and processing PDF...");

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        setUploadMessage(
          `PDF processed successfully! ${data.total_chunks} chunks created.`
        );

        // Start fresh chat for the new document
        setMessages([]);
        setQuestion("");
      } else {
        setUploadMessage("Failed to process PDF.");
      }
    } catch (error) {
      setUploadMessage(
        "Could not connect to the backend. Make sure FastAPI is running."
      );
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);

      const currentQuestion = question;

      const response = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(
          currentQuestion
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (data.answer) {
        // Add question + answer to the SAME chat
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            question: currentQuestion,
            answer: data.answer,
          },
        ]);

        setQuestion("");
      } else {
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            question: currentQuestion,
            answer:
              data.error || "Something went wrong.",
          },
        ]);

        setQuestion("");
      }
    } catch (error) {
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          question,
          answer:
            "Could not connect to the backend. Make sure FastAPI is running.",
        },
      ]);

      setQuestion("");
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app-container">

      {/* Header */}

      <div className="header">

        <div className="logo">
          📄
        </div>

        <div>
          <h1>Document AI Chatbot</h1>

          <p>
            Ask questions about your uploaded PDF
          </p>
        </div>

      </div>

      {/* Upload Section */}

      <div className="section">

        <h2>📤 Upload Document</h2>

        <p className="section-description">
          Upload a PDF document to start asking
          questions.
        </p>

        <div className="upload-area">

          <input
            className="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />

          {selectedFile && (
            <div className="selected-file">
              📄 {selectedFile.name}
            </div>
          )}

          <button
            className="primary-button"
            onClick={handleUpload}
          >
            Upload PDF
          </button>

        </div>

        {uploadMessage && (
          <div className="upload-message">
            {uploadMessage}
          </div>
        )}

      </div>

      {/* Chat Section */}

      <div className="section chat-section">

        <div className="chat-header">

          <div>
            <h2>💬 Ask Questions</h2>

            <p className="section-description">
              Ask anything about your document.
            </p>
          </div>

          {messages.length > 0 && (
            <button
              className="clear-button"
              onClick={handleClearChat}
            >
              🗑 Clear Chat
            </button>
          )}

        </div>

        {/* Chat History */}

        <div className="chat-history">

          {messages.length === 0 ? (
            <div className="empty-chat">

              <div className="empty-icon">
                🤖
              </div>

              <h3>
                Your conversation will appear here
              </h3>

              <p>
                Upload a PDF and ask your first
                question.
              </p>

            </div>
          ) : (
            messages.map((message, index) => (

              <div
                className="chat-message"
                key={index}
              >

                {/* User */}

                <div className="message user-message">

                  <div className="avatar user-avatar">
                    You
                  </div>

                  <div className="message-body">

                    <span className="message-name">
                      You
                    </span>

                    <p>
                      {message.question}
                    </p>

                  </div>

                </div>

                {/* AI */}

                <div className="message bot-message">

                  <div className="avatar bot-avatar">
                    AI
                  </div>

                  <div className="message-body">

                    <span className="message-name">
                      Document AI
                    </span>

                    <p>
                      {message.answer}
                    </p>

                  </div>

                </div>

              </div>

            ))
          )}

          {/* Loading */}

          {loading && (
            <div className="message bot-message">

              <div className="avatar bot-avatar">
                AI
              </div>

              <div className="message-body">

                <span className="message-name">
                  Document AI
                </span>

                <div className="loading">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span className="loading-text">
                    Thinking...
                  </span>
                </div>

              </div>

            </div>
          )}

        </div>

        {/* Question Input */}

        <div className="question-area">

          <input
            className="question-input"
            type="text"
            placeholder="Ask something about your document..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleAsk();
              }
            }}
          />

          <button
            className="ask-button"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>

        </div>

        <div className="input-hint">
          Press Enter to send
        </div>

      </div>

      {/* Footer */}

      <div className="footer">
        Powered by RAG • FAISS • Sentence Transformers • Llama 3.2
      </div>

    </div>
  );
}

export default App;