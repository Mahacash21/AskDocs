# step 1 imports
import streamlit as st
from ingest import ingest_document
from rag import ask
import os

# step 2 - page title
st.title("AskDocs")
st.write("Upload a PDF document and ask questions about its content!")

# initialize session state  to track if a document has been ingested
if "ingested" not in st.session_state:     
    st.session_state.ingested = False

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None


#step 3 - file uploader  uploaded file object in memory we need to build the file path and save it to disk so that we can pass the file path to the ingest function
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and not st.session_state.ingested:  # if a file is uploaded and not ingested yet
    file_path = os.path.join("docs", uploaded_file.name)  # save the uploaded file to a docs location
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    collection_name = os.path.splitext(uploaded_file.name)[0]  # removes .pdf extension
    collection_name = collection_name.replace(" ", "_").lower()
    count = ingest_document(file_path, collection_name=collection_name) #  get the number of chunks ingested
    st.session_state.collection_name = collection_name  # store the collection name in session state for later use
    st.success(f" ingested {count} chunks. Document ingested successfully! You can now ask questions about it.")
    st.session_state.ingested = True

if st.session_state.ingested:
    question = st.text_input("Ask a question about the document:")
    if question:
        answer = ask(question, collection=st.session_state.collection_name)  # get the answer from the ask function 
        st.write("Answer:", answer)  # display the answer on the page
