from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Function to create a vector store from text chunks
# Converts each chunk into embeddings and stores them in FAISS for fast similarity search

def create_vector_stores(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # HuggingFace embeddings using fast sentence transformer model
    db = FAISS.from_texts(
        [d["text"] for d in chunks],
        embedding=embeddings,
        metadatas=[d["metadata"] for d in chunks]
    )
    db.save_local('faiss_index')  # Save the vector store locally so it can be loaded later without recomputation


# Function to load the previously saved FAISS vector store

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )