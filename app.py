# step 1 imports   from other modeules and libraries we need
import streamlit as st
from ingest import ingest_document
from rag import ask
import os

# step 2 - page title
st.title("AskDocs")
# security check for confidential documents warning
st.caption("⚠️ Do not upload confidential documents. Content is sent to OpenAI for processing.")
st.write("Upload a PDF document and ask questions about its content!")

# initialize session state  to track if a document has been ingested
if "ingested" not in st.session_state:     
    st.session_state.ingested = False

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

if "question_count" not in st.session_state:
    st.session_state.question_count = 0


#step 3 - file uploader  uploaded file object in memory we need to build the file path and save it to disk so that we can pass the file path to the ingest function
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


# security check for file size limit 10MB
if uploaded_file is not None:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File too large. Max 10MB allowed.")
        st.stop()

# if a file is uploaded and not ingested yet
if uploaded_file is not None and not st.session_state.ingested:  
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
        # security check for question length and limit the number of questions per session
        if len(question) > 500:
             st.error("Question too long. Max 500 characters.")
             st.stop()
        if st.session_state.question_count >= 10:
             st.error("Question limit reached for this session.")
             st.stop()
        st.session_state.question_count += 1
        result = ask(question, collection=st.session_state.collection_name)
        st.write("Answer:", result["answer"])
        
        with st.expander("📄 View sources"):
            for i, source in enumerate(result["sources"], 1):
                st.write(f"**Source {i}:**")
                st.write(source)
                st.write("---")