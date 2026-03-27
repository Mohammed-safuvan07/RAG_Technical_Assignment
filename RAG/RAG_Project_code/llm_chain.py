from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


# Define a prompt template for the HR assistant
# {history} → previous conversation (chat memory)
# {context} → relevant document chunks retrieved from vector store
# {question} → user’s current query
def get_chain(api_key):
    prompt = PromptTemplate.from_template("""
    You are an HR assistant.

    Previous conversation:
    {history}                                           
    
    Use the context below to answer the question.
    If answer not in context, say:
    "Answer is not available in the context."
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """)

    # Google Gemini LLM for text generation
    # temperature=0.2 : keeps responses more focused and deterministic
    # top_k=50 : considers top 50 token options during generation (controls diversity)
    # top_p=0.9 : nucleus sampling, considers 90% cumulative probability of token choices

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",google_api_key=api_key, temperature=0.2,top_k=50,top_p=0.9
    )

    return prompt | llm    # Combine the prompt template and LLM into a chain