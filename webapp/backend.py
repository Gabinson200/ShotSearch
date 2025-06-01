import os
from dotenv import load_dotenv # For loading API key from .env file
import numpy as np # For accurately getting data type size for embeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS # Or from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def initialize_rag_chain():
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
    # This line already prints the number of chunks
    print(f"Created {len(chunks)} chunks.")
    if not chunks:
        print("No chunks created. The document might be too small or there's an issue with splitting.")
        return

    # --- Initialize Embedding Model (needed for memory calculation and FAISS) ---
    print("Initializing embedding model (all-MiniLM-L6-v2)...")
    try:
        embeddings_model_name = "all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        return

    # --- Calculate and Print Embedding Memory Footprint ---
    if chunks and embeddings:
        try:
            # Get dimensionality from the embedding model by embedding a sample query
            sample_embedding = embeddings.embed_query("sample to get dimensionality")
            dimensionality = len(sample_embedding)
            # Determine bytes per dimension (usually 4 for float32, which is common)
            # np.dtype(type(sample_embedding[0])).itemsize is more robust
            bytes_per_dimension = np.dtype(type(sample_embedding[0])).itemsize

            num_chunks = len(chunks)
            estimated_raw_vector_memory_bytes = num_chunks * dimensionality * bytes_per_dimension
            estimated_raw_vector_memory_kb = estimated_raw_vector_memory_bytes / 1024
            estimated_raw_vector_memory_mb = estimated_raw_vector_memory_kb / 1024

            print(f"\n--- Raw Embedding Vector Memory Estimation ---")
            print(f"Number of document chunks: {num_chunks}")
            print(f"Embedding dimensionality: {dimensionality}")
            print(f"Bytes per dimension (e.g., float32): {bytes_per_dimension}")
            print(f"Estimated memory for raw embedding vectors: {estimated_raw_vector_memory_bytes} bytes")
            print(f"                                         ~= {estimated_raw_vector_memory_kb:.2f} KB")
            print(f"                                         ~= {estimated_raw_vector_memory_mb:.2f} MB")
            print(f"---")
        except Exception as e:
            print(f"Could not calculate embedding memory footprint: {e}")


    # --- 3. Create Embeddings and Vector Store (using local embeddings) ---
    # The print statement below was part of step 3, moving the model init above
    print("\nCreating vector store with local HuggingFaceEmbeddings (all-MiniLM-L6-v2)...")
    try:
        # Using FAISS as the vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        # If using ChromaDB instead:
        # from langchain_community.vectorstores import Chroma
        # vector_store = Chroma.from_documents(chunks, embeddings)
        # print("Using ChromaDB as vector store.")
        print("Vector store created successfully.")
    except Exception as e:
        print(f"Error creating embeddings or vector store: {e}")
        return

    # --- 4. Create a Retriever ---
    # This component will fetch relevant documents from the vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 chunks

    # --- 5. Set up the LLM (Using OpenAI API) ---
    print("Initializing OpenAI LLM (gpt-4o-mini)...") # Updated model name in print
    try:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=openai_api_key)
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

    return rag_chain

def get_vaccination_info(rag_chain, question):
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        print(f"Error during RAG chain invocation: {e}")
        return None