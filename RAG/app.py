import streamlit as st
from RAG_Project_code.ingestion import load_documents
from RAG_Project_code.splitter import get_text_chunks
from RAG_Project_code.embeddings import create_vector_stores, load_vector_store
from RAG_Project_code.chain import get_chain

# Initialize session state for conversation history
if "history" not in st.session_state:
    st.session_state.history = []

if "processed" not in st.session_state:
    st.session_state.processed = False

st.set_page_config(page_title="HR Policy RAG Assistant")

st.title("HR Policy RAG Assistant")

# Sidebar: Documnets Upload and LLM API key
with st.sidebar:
    st.header("Upload HR Documents & API Key")
    api_key = st.text_input("Enter Google API Key", type="password")
    files = st.file_uploader(
        "Upload PDF, DOCX, TXT", accept_multiple_files=True
    )

    if st.button("Process Documents") and files:  # Process documents and create vector store for RAG
        if not api_key:
            st.warning("Please enter your Google API Key first!")
        else:
            with st.spinner("Processing documents..."):
                text = load_documents(files)         # Load document content and metadata
                chunks = get_text_chunks(text)       # Split text into chunks for embeddings
                create_vector_stores(chunks)         # Generate embeddings and store in FAISS vector database
                st.success("Documents processed!")
                st.session_state.processed = True

# Main area: Chat interface
user_question = st.text_area("Ask a question from documents", height=100)

if st.button("Ask") and user_question:
    if not api_key:
        st.warning("Please enter your Google API Key!")
    elif not st.session_state.processed:
        st.warning("Please process documents first!")
    else:
        with st.spinner("Generating answer..."):
            db = load_vector_store()                          # Load vector store and perform similarity search
            docs = db.similarity_search(user_question, k=2)

            chain = get_chain(api_key)

            history_text = ""
            for chat in st.session_state.history:
                history_text += f"User: {chat['question']}\n Assistant: {chat['answer']} \n"

            response = chain.invoke({
                "context": "\n\n".join([doc.page_content for doc in docs]),
                "question": user_question,
                "history": history_text
            })

            # Display sources
            st.write("### Sources")
            for doc in docs:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                snippet = doc.page_content[:100].replace("\n", " ")
                st.write(f"- {source} | Page: {page} | {snippet}")

            # Display the answer from the assistant
            st.write("### Answer")
            st.write(response.content)

            # Append question and answer to session history
            st.session_state.history.append(
                {"question": user_question, "answer": response.content}
            )

# Display conversation history
if st.session_state.history:
    with st.expander("Conversation History", expanded=False):
        for chat in st.session_state.history:
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**Assistant:** {chat['answer']}")
            st.write("---")