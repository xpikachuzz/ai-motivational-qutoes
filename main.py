from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL for better security
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model and FAISS index once
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('quotes_faiss.index')

# Load quotes lookup once
with open('quotes_lookup.txt', 'r', encoding='utf-8') as f:
    quotes = [line.strip() for line in f.readlines()]

# Request body schema
class SearchQuery(BaseModel):
    text: str
    k: int = 5

@app.get("/")
def home():
    return {"message": "Quote Vector Search API is running."}

@app.post("/search/")
def search(query: SearchQuery):
    # Embed query dynamically
    query_vector = model.encode([query.text], convert_to_numpy=True).astype('float32')

    # Search in FAISS index
    D, I = index.search(query_vector, query.k)

    # Prepare results
    results = [quotes[idx] for idx in I[0]]

    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
