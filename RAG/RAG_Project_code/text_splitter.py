from langchain_text_splitters import RecursiveCharacterTextSplitter

# Function to split documents into smaller text chunks for semantic search
def get_text_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)   # Initialize a text splitter with chunk size of 1000 characters
                                                                                    # and an overlap of 200 characters to maintain context across chunks
    chunks = []

    for doc in docs:
        split_texts = splitter.split_text(doc["text"])
        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })

    return chunks
