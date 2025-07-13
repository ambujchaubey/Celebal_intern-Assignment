import streamlit as st
import requests
import webbrowser
import threading

API_URL = "http://127.0.0.1:8000"

st.title("RAG Q&A Chatbot")

# PDF Upload
st.header("1. Upload a PDF")
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
if pdf_file:
    with st.spinner("Uploading and processing PDF..."):
        files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
        resp = requests.post(f"{API_URL}/ingest_pdf/", files=files)
        if resp.ok:
            st.success(f"PDF processed! Chunks: {resp.json().get('chunks')}")
        else:
            st.error(f"Error: {resp.text}")

# Ask a Question
st.header("2. Ask a Question")
question = st.text_input("Your question:")
if st.button("Ask") and question:
    with st.spinner("Getting answer..."):
        resp = requests.post(f"{API_URL}/ask/", data={"question": question})
        if resp.ok:
            st.markdown(f"**Answer:** {resp.json().get('answer')}")
        else:
            st.error(f"Error: {resp.text}")

# Auto-open browser if run directly
if __name__ == "__main__":
    def open_browser():
        webbrowser.open_new("http://localhost:8501")
    threading.Timer(1.5, open_browser).start() 