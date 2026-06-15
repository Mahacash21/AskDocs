'''
1. imports
2. define split_into_chunks()
3. load PDF → build complete_text  (loop here)
4. chunks = list(split_into_chunks(complete_text))
5. model = SentenceTransformer(...)
6. embedding = model.encode(chunks)
7. client = chromadb.PersistentClient(...)
8. collection = client.get_or_create_collection(...)
9. collection.add(ids, embeddings, documents)
10. print(f"Stored {len(chunks)} chunks")
'''
# Main Block
#1. imports
from pypdf import PdfReader   #read the PDF file
from sentence_transformers import SentenceTransformer   #for embedding the text
import chromadb
#from torch import chunk    #vector database
#import os  #for file handling


model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Chunk splitting function to split the text into manageable pieces for embedding
def split_into_chunks(text, chunk_size=500, overlap=50):
    """Split the text into chunks of specified size with overlap."""
    start = 0
    while start < len(text):
        end = start + chunk_size
        yield text[start:end]
        start += chunk_size - overlap


def ingest_document(file_path, collection_name="askdocs"):

    #3. read the PDF file
    document = PdfReader(file_path)  

    # 4. load the PDF file and extract text from each page
    Complete_text = ""
    for page in document.pages:  #iterate through each page
        text = page.extract_text()  #extract text from the page
        Complete_text += text  #append the text to the complete text variable

    # 5. split the text into chunks
    chunks = list(split_into_chunks(Complete_text))  

    # 6. embed the chunks
    embedding = model.encode(chunks)  #embed the chunk

    # 7. initialize ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")

    # 8. create or get the collection and insert the embeddings with metadata
    collection = client.get_or_create_collection(collection_name) 

    # 9. insert the embeddings and metadata into the collection
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embedding,
        documents=chunks
    )
    return len(chunks)

'''
This is the explaination of the if __name__ == "__main__": block in Python.
The concept is called "module guard" or "entry point check"
Every Python file has a built-in variable called __name__. Python sets it automatically depending on how the file is being used.

Two scenarios:
Scenario 1 — You run the file directly
python ingest.py
Python sets __name__ = "__main__" — so the if block runs.
Scenario 2 — Another file imports it
pythonfrom ingest import ingest_document  # inside app.py
Python sets __name__ = "ingest" — so the if block is skipped. Only the function is loaded.

'''

if __name__ == "__main__":
    count = ingest_document("C:\\Users\\praka\\OneDrive\\Desktop\\Projects\\AskDocs\\docs\\10050-medicare-and-you.pdf")
    print(f"✅ Stored {count} chunks into ChromaDB")


