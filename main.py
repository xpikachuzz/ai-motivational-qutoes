from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sentence_transformers import SentenceTransformer
import uvicorn

app = FastAPI()

# Load quotes.txt
quotes = []
authors = []

with open("quotes.txt", encoding="utf-8") as f:
    for line in f:
        if ':' in line:
            author, quote = line.strip().split(':', 1)
            authors.append(author.strip())
            quotes.append(quote.strip())

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed all quotes once
quote_embeddings = model.encode(quotes)

# API request schema
class Query(BaseModel):
    text: str
    k: int = 5

@app.get("/")
def home():
    return {"message": "Quote Vector Search API is running."}

@app.post("/search/")
def search(query: Query):
    query_embedding = model.encode([query.text])[0]

    # Compute cosine similarity
    similarities = np.dot(quote_embeddings, query_embedding) / (
        np.linalg.norm(quote_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    top_indices = np.argsort(similarities)[::-1][:query.k]

    results = []
    for idx in top_indices:
        results.append({
            "author": authors[idx],
            "quote": quotes[idx],
            "score": float(similarities[idx])
        })

    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
