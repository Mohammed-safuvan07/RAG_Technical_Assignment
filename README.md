#                                            HR Policy RAG Assistant

## AI/ML Engineer Technical Assignment – Retrieval Augmented Generation (RAG) Chatbot

This project implements a Retrieval-Augmented Generation (RAG) based HR assistant that answers employee questions from HR policy documents such as Leave Policy, Work Hours, and Notice Period.

The system retrieves relevant content from uploaded documents and uses a Large Language Model to generate context-aware answers grounded strictly in document content.


# 🛠️ Environment Setup
Step 1 - Create Virtual Environment


      RAG_Project\Scripts\activate


Step 2 - Activate Environment


      RAG_Project\Scripts\activate


Step 3 - Install Dependencies


      pip install -r requirements.txt


## Running the Application


streamlit run app.py


Open in browser:  http://localhost:8501

# 🧠 Architecture Overview (RAG Pipeline)

This system follows a complete RAG architecture:

## 1. Document Upload

Users upload HR documents in:
 * PDF
 * DOCX
 * TXT

## 2. Text Extraction (ingestion.py)

   * Extracts text from each document
   * Preserves metadata: source file name and page number

## 3. Text Chunking (splitter.py)

  * Uses RecursiveCharacterTextSplitter
  * Chunk size: 1000
  * Overlap: 200
  * Ensures semantic continuity between chunks

# 4. Embedding Generation (embeddings.py)

  * Uses HuggingFace model: all-MiniLM-L6-v2
  * Converts text chunks into vector embeddings

# 5. Vector Database (FAISS)
  * Stores embeddings locally
  * Enables fast similarity search for retrieval

# 6. Query Retrieval

  When a user asks a question:
  Question is embedded
  Top 2 most similar chunks are retrieved from FAISS

# 7. LLM Response Generation (chain.py)
  Google Gemini (gemini-2.5-flash) is used
  ## Prompt includes:
      Conversation history
      Retrieved document context
      User question
      Model parameters:
      temperature = 0.2
      top_k = 50
      top_p = 0.9

# 8. Streamlit Chat Interface (app.py)
  Upload documents
  Ask questions
  View answers
  View source citations (file + page + snippet)
  Maintains conversation history


# Key Features Implemented

  Multi-document upload from UI
  Metadata tracking (source & page number)
  Semantic chunking
  HuggingFace embeddings
  FAISS vector database
  Grounded LLM responses
  Conversation memory
  Source citation in answers


# ❓ Sample Questions to Test

  1. Tell me about the leave policy for new joiners ?
  2.  what if it is their birthday on the day they join?
  3.   Employment contract details ?
  
# Assumptions & Limitations

  1. Only supports English HR documents
  2. Assumes documents contain clear, structured, machine-readable text (not scanned images)
  3. RAG performance depends on the quality and completeness of the uploaded documents
  4. If information is missing or unclear in documents, the system responds:
     "Answer is not available in the context.”

# 🚀 Future Improvements

  1. Support for multi-language HR documents
  2. Support for multi-language HR documents
  3. Add an evaluation dashboard for testing query quality
  4. Integrate scalable vector databases like Pinecone or Chroma

# Design Decisions

  * Streamlit chosen for quick UI development and multi-file upload support
  * FAISS used for fast and lightweight local vector similarity search
  * Chunk size (1000) and overlap (200) tuned to balance context retention and retrieval accuracy
  * Expandable conversation history for a clean user interface
  * HuggingFace embeddings used to avoid paid embedding APIs
  * Gemini Flash selected for fast and cost-effective response generation
