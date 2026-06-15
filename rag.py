'''
Step 1 — Take a question
A simple string input — "What does Medicare cover?"
Step 2 — Embed the question
Use the same SentenceTransformer model from ingest.py to convert the question into a vector. Must be the same model — otherwise the numbers won't match.
Step 3 — Search ChromaDB
Query the collection with that vector. Ask for the top 3 most similar chunks. ChromaDB compares your question vector against all 671 chunk vectors and returns the closest matches.
Step 4 — Build a prompt
Combine the retrieved chunks + the question into one prompt that says:
Here is some context: [chunks]
Answer this question using only the context above: [question]
Step 5 — Call OpenAI and return the answer
Send that prompt to gpt-3.5-turbo and return the response.
'''

import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

model = SentenceTransformer('all-MiniLM-L6-v2')

def ask(question, collection = 'askdocs'):
    embedding = model.encode(question).tolist()  # step 2 embed the question into a vector
    client = chromadb.PersistentClient(path="chroma_db") # connect to the ChromaDB database
    collection = client.get_or_create_collection(name=collection) #  get the collection we created in ingest.py
    results = collection.query(          # Step3 : search for the most similar chunks to the question
        query_embeddings=[embedding],
        n_results=3
    )
    # step 4 : build a prompt with the retrieved chunks and the question
    
    chunks = results['documents'][0]    # get the retrieved chunks from the query results there are 3 chunks in the list
    
    context = "\n\n".join(chunks)   # combine the chunks into a single string with newlines in between
    prompt = f"Here is some context: {context}\n\nAnswer this question using only the context above: {question}"
    
    # step 5 : call OpenAI and return the answer
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "Answer only using the context provided."},
          {"role": "user", "content": prompt}
      ]
   )
    return response.choices[0].message.content
    
    
if __name__ == "__main__":
    print(ask("What does Medicare cover?")) 




