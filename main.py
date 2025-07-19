from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load FAISS index
index = faiss.read_index("index.faiss")

# Load lookup file
with open("lookup.txt", "r", encoding="utf-8") as f:
    lookup = [line.strip() for line in f]

# Load sentence embedding model (uses a pre-trained model)
model = SentenceTransformer('all-MiniLM-L6-v2')

class Query(BaseModel):
    text: str
    k: int = 5  # number of results to return

@app.post("/search/")
def search(query: Query):
    # Convert query text to embedding vector
    vector = model.encode([query.text])[0].astype('float32')

    # Search FAISS index
    distances, indices = index.search(np.array([vector]), query.k)

    # Map indices to lookup results
    results = []
    for idx in indices[0]:
        if 0 <= idx < len(lookup):
            results.append(lookup[idx])
        else:
            results.append("Unknown")

    return {"results": results, "distances": distances[0].tolist()}
