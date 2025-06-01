import os
from dotenv import load_dotenv # For loading API key from .env file

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS # Or from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check if the OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
        print("Please create a .env file and add your OPENAI_API_KEY, or set it as an environment variable.")
        return

    # --- 1. Load Your Document ---
    print("Loading document (my_document.txt)...")
    try:
        loader = TextLoader("./my_document.txt", encoding="utf-8") # Specify encoding
        documents = loader.load()
    except Exception as e:
        print(f"Error loading document: {e}")
        return

    if not documents:
        print("No documents loaded. Check if 'my_document.txt' exists and is not empty.")
        return

    # --- 2. Split Document into Chunks ---
    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100) # Adjusted overlap
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    if not chunks:
        print("No chunks created. The document might be too small or there's an issue with splitting.")
        return

    # --- 3. Create Embeddings and Vector Store (using local embeddings) ---
    print("Creating embeddings and vector store with local HuggingFaceEmbeddings (all-MiniLM-L6-v2)...")
    try:
        embeddings_model_name = "all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

        # Using FAISS as the vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        # If using ChromaDB instead:
        # from langchain_community.vectorstores import Chroma
        # vector_store = Chroma.from_documents(chunks, embeddings)
        # print("Using ChromaDB as vector store.")
    except Exception as e:
        print(f"Error creating embeddings or vector store: {e}")
        return

    # --- 4. Create a Retriever ---
    # This component will fetch relevant documents from the vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 chunks

    # --- 5. Set up the LLM (Using OpenAI API) ---
    print("Initializing OpenAI LLM (gpt-3.5-turbo)...")
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=openai_api_key)
        # Other options: "gpt-4o-mini", "gpt-4-turbo", etc.
    except Exception as e:
        print(f"Error initializing OpenAI LLM: {e}")
        return

    # --- 6. Create a Prompt Template ---
    prompt_template_str = """
    You are an assistant for question-answering tasks.
    Use only the following pieces of retrieved context to answer the question.
    If you don't know the answer from the context, just say that you don't know.
    Do not make up an answer. Keep the answer concise.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template_str)

    # --- 7. Build the RAG Chain ---
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # --- 8. Ask a Question ---
    print("\nSimple RAG with OpenAI is ready!")
    print("Ask a question about the content in 'my_document.txt'. Type 'exit' to quit.")

    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'exit':
            break
        if not user_question.strip():
            print("Please enter a question.")
            continue

        print("Thinking...")
        try:
            response = rag_chain.invoke(user_question)
            print("\nAnswer:", response)
        except Exception as e:
            print(f"Error during RAG chain invocation: {e}")
            print("This might be due to API issues or configuration problems.")

        print("-" * 40)

if __name__ == "__main__":
    main()