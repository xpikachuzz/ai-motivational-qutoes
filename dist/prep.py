import boto3
import faiss
import numpy as np
import json

# Load index and lookup once (reuse between invocations)
index = faiss.read_index("/tmp/quotes_faiss.index")
with open("/tmp/quotes_lookup.txt", "r") as f:
    lookup = [line.strip() for line in f.readlines()]

def lambda_handler(event, context):
    query = event['queryStringParameters'].get('q', '')
    if not query:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing query"})}

    # Convert query into embedding here
    # Example: vector = your_embedding_function(query)
    vector = np.random.random((512)).astype('float32')  # Replace this

    D, I = index.search(np.array([vector]), k=5)
    results = [lookup[i] for i in I[0]]

    return {
        "statusCode": 200,
        "body": json.dumps({"results": results})
    }
