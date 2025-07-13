from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import faiss
import os
import tempfile
from pypdf import PdfReader
import webbrowser
import threading

app = FastAPI()

@app.get("/")
def root():
    return {"status": "RAG Q&A API is running"}

# Load embedding model
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    embedder = None
    print(f"Error loading embedding model: {e}")

# Load LLM (TinyLlama or Phi-2)
llm_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # or try "microsoft/phi-2"
try:
    tokenizer = AutoTokenizer.from_pretrained(llm_model)
    llm = AutoModelForCausalLM.from_pretrained(llm_model)
    gen_pipeline = pipeline("text-generation", model=llm, tokenizer=tokenizer, max_new_tokens=256)
except Exception as e:
    gen_pipeline = None
    print(f"Error loading LLM: {e}")

# In-memory store for simplicity
doc_chunks = []
chunk_embeddings = None
index = None
chunk_texts = []

# Helper: extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Helper: chunk text
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

@app.post("/ingest_pdf/")
async def ingest_pdf(file: UploadFile = File(...)):
    if embedder is None:
        return JSONResponse({"error": "Embedding model not loaded."}, status_code=500)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)
    if not text.strip():
        return JSONResponse({"error": "No text extracted from PDF."}, status_code=400)
    global doc_chunks, chunk_embeddings, index, chunk_texts
    doc_chunks = chunk_text(text)
    chunk_texts = doc_chunks
    chunk_embeddings = embedder.encode(doc_chunks, convert_to_numpy=True)
    index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
    index.add(chunk_embeddings)
    return {"chunks": len(doc_chunks)}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    if gen_pipeline is None:
        return JSONResponse({"error": "LLM not loaded."}, status_code=500)
    global chunk_embeddings, index, chunk_texts
    if index is None:
        return JSONResponse({"error": "No documents ingested yet."}, status_code=400)
    q_emb = embedder.encode([question], convert_to_numpy=True)
    D, I = index.search(q_emb, 3)  # top 3 chunks
    context = "\n".join([chunk_texts[i] for i in I[0]])
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    answer = gen_pipeline(prompt)[0]["generated_text"][len(prompt):].strip()
    return {"answer": answer}

# Auto-open browser to docs on server start
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/docs")

def run_browser_thread():
    threading.Timer(1.5, open_browser).start()

run_browser_thread() 