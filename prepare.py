import csv
import json
import os 


def csv_to_quote_txt(csv_file_path, output_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        with open(output_file_path, 'w', encoding='utf-8') as txtfile:
            for row in reader:
                if len(row) >= 2:
                    author,quote  = row[0].strip(), row[1].strip()
                    if len(author) == 0:
                        author = "Unkown"

# csv_to_quote_txt('./raw/quotes.csv', './processed/quotes.txt')


def chatgpt_txt_to_quote_txt(csv_file_path, output_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        with open(output_file_path, 'w', encoding='utf-8') as txtfile:
            for row in f:
                row = row.strip().split(" — ")
                quote = row[0]
                author = "Unknow"
                if len(row) == 2:
                    author = row[1]
                txtfile.write(f"{author}:{quote}\n")


#chatgpt_txt_to_quote_txt('./raw/chatgpt.txt', './processed/chatgpt_quotes.txt')

def AnimeQuotes():
    with open("./raw/AnimeQuotes.csv", 'r', encoding='utf-8') as f:
        with open("./processed/anime_quotes.txt", 'w', encoding='utf-8') as txtfile:
            for row in f:
                row = row.split(",")
                character = row[-2]
                quote = ",".join(row[:-2])
                txtfile.write(f"{character}:{quote}\n")


#AnimeQuotes()

def quotesJson():
    with open("./raw/quotes.json", 'r', encoding='utf-8') as json_data:
        with open("./processed/quotes_json.txt", 'w', encoding='utf-8') as txtfile:
            d = json.load(json_data)
            for obj in d:
                quote, author = obj['Quote'], obj['Author']
                txtfile.write(f"{author}:{quote}\n")

def quotesJson():
    with open("./raw/quotes.json", 'r', encoding='utf-8') as json_data:
        with open("./processed/quotes_json.txt", 'w', encoding='utf-8') as txtfile:
            d = json.load(json_data)
            for obj in d:
                quote, author = obj['Quote'], obj['Author']
                txtfile.write(f"{author}:{quote}\n")

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load quotes.txt
authors = []
quotes = []

with open('quotes.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if ':' in line:
            author, quote = line.strip().split(':', 1)
            authors.append(author.strip())
            quotes.append(quote.strip())

# Save lookup file (optional but useful)
with open('quotes_lookup.txt', 'w', encoding='utf-8') as f:
    for author, quote in zip(authors, quotes):
        f.write(f"{author}:{quote}\n")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(quotes).astype('float32')

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, 'quotes_faiss.index')

print(f"Index built and saved with {index.ntotal} quotes.")
