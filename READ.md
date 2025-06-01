# Simple RAG with OpenAI and Local Embeddings

This project demonstrates a simple Retrieval Augmented Generation (RAG) application
using Python, LangChain, an OpenAI LLM (via API), and local sentence embeddings
with a FAISS vector store.

## Features

- Loads data from a local text file (`my_document.txt`).
- Chunks the document for processing.
- Uses local `sentence-transformers` for creating text embeddings (free).
- Stores embeddings in a local FAISS vector store (in-memory).
- Retrieves relevant chunks based on user query.
- Uses an OpenAI LLM (e.g., `gpt-3.5-turbo`) via API to generate answers based on the retrieved context.

## Project Structure

simple-rag-openai/
├── venv/                   # Python virtual environment (ignored by git)
├── app.py                  # Main application script
├── my_document.txt         # Sample data file
├── requirements.txt        # Python dependencies
├── .env                    # For storing OPENAI_API_KEY (ignored by git)
├── .gitignore              # Specifies intentionally untracked files by Git
└── README.md               # This file

## Setup Instructions

1.  **Clone the Repository (or create files manually as described):**
    ```bash
    # If you're cloning from GitHub (after pushing it)
    # git clone [https://github.com/YOUR_USERNAME/simple-rag-openai.git](https://github.com/YOUR_USERNAME/simple-rag-openai.git)
    # cd simple-rag-openai
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    # .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up OpenAI API Key:**
    Create a file named `.env` in the root of the project directory (`simple-rag-openai/`) and add your OpenAI API key:
    ```env
    OPENAI_API_KEY="sk-your_actual_openai_api_key_here"
    ```
    Replace `sk-your_actual_openai_api_key_here` with your real API key.
    **Important:** The `.env` file is listed in `.gitignore` and should NOT be committed to GitHub.

5.  **Prepare Your Data (Optional):**
    Modify `my_document.txt` with the text content you want the RAG system to use as its knowledge base.

## How to Run

1.  Ensure your virtual environment is activated.
2.  Ensure your `.env` file is set up with your `OPENAI_API_KEY`.
3.  Run the application:
    ```bash
    python app.py
    ```
4.  The script will load the document, process it, and then prompt you to ask questions. Type `exit` to quit.

## Example Usage

Loading document (my_document.txt)...
Splitting document into chunks...
Created 2 chunks.
Creating embeddings and vector store with local HuggingFaceEmbeddings (all-MiniLM-L6-v2)...
Initializing OpenAI LLM (gpt-3.5-turbo)...

Simple RAG with OpenAI is ready!
Ask a question about the content in 'my_document.txt'. Type 'exit' to quit.

Your question: What is the capital of France?
Thinking...
Answer: The capital of France is Paris.

Your question: What is Berlin known for?
Thinking...
Answer: Berlin is the capital of Germany and a major cultural hub. The Brandenburg Gate is a famous landmark in Berlin.

Your question: exit


## Notes

-   This is a basic implementation. For production, consider more robust error handling, logging, and potentially more advanced RAG techniques.
-   OpenAI API usage will incur costs based on your usage.
-   The local embedding model (`all-MiniLM-L6-v2`) is downloaded the first time it's used.
-   FAISS vector store is in-memory for this example. For persistence across sessions with FAISS, you would need to explicitly save and load the index. ChromaDB can be configured to persist to disk more easily if needed.