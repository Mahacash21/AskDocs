AskDocs 📄

Upload any PDF and ask questions about it in plain English. AskDocs uses RAG (Retrieval-Augmented Generation) to find the most relevant parts of your document and generate accurate, grounded answers using OpenAI.


What it does


Upload a PDF through a simple web interface
The document is chunked, embedded, and stored in a local vector database
Ask any question about the document in natural language
Get answers generated from the actual content of your PDF — not hallucinated



How it works

PDF → extract text → chunk → embed → store in ChromaDB
Question → embed → similarity search → retrieve top 3 chunks → GPT-3.5 → answer

Stack:


pypdf — PDF text extraction
sentence-transformers — text embeddings (all-MiniLM-L6-v2)
ChromaDB — local vector database
OpenAI GPT-3.5-turbo — answer generation
Streamlit — web UI



Project structure

AskDocs/
├── app.py          # Streamlit UI
├── ingest.py       # PDF loading, chunking, embedding, storing
├── rag.py          # Question embedding, similarity search, OpenAI call
├── .env            # API keys (never commit this)
├── .gitignore
├── requirements.txt
├── docs/           # uploaded PDFs stored here
└── chroma_db/      # vector database stored here


Setup

1. Clone the repo

bashgit clone https://github.com/yourusername/AskDocs.git
cd AskDocs

2. Create and activate a virtual environment

bashpython -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate

3. Install dependencies

bashpip install -r requirements.txt

4. Add your OpenAI API key

Create a .env file in the root folder:

OPENAI_API_KEY=your_key_here

Get your key at platform.openai.com

5. Create the docs folder

bashmkdir docs

6. Run the app

bashstreamlit run app.py

Open your browser at http://localhost:8501


Usage


Upload a PDF using the file uploader
Wait for the success message showing how many chunks were ingested
Type your question in the text box
Read the answer — generated from your document


Each document is stored in its own ChromaDB collection named after the file, so answers are always scoped to the uploaded document.


Requirements

openai
chromadb
pypdf
sentence-transformers
streamlit
python-dotenv


Future improvements


 Support .txt and .docx files
 Show source chunks used to generate the answer
 Chat history within a session
 Multiple document support
 Deploy to Streamlit Community Cloud



Built with

Built as a portfolio project to demonstrate RAG (Retrieval-Augmented Generation) using Python, ChromaDB, and the OpenAI API.