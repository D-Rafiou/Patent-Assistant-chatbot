from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

data = "./output/output.json"
chunks = []

with open(data, "r", encoding="utf-8") as file:
    chunks = json.load(file)

# generate embeddings 
content = [chunk["content"] for chunk in chunks]
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(content,show_progress_bar=True)

embeddings_np = np.array(embeddings).astype("float32")
faiss.normalize_L2(embeddings_np)
index = faiss.IndexFlatIP(embeddings_np.shape[1])
index.add(embeddings_np)
# we make dictionary that maps index to chunk 
chunk_map = {i:chunk for i,chunk in enumerate(chunks)}
query = "how long does it take to register a patent"
query_vec  = model.encode([query],show_progress_bar=True)
faiss.normalize_L2(query_vec)
k = 5
distances,indices = index.search(query_vec,k)
for idx in indices[0]:
    chunk = chunk_map[idx]
    print(f"Content: {chunk['content']}")
    print(f"chunk index: {chunk['metadata']['chunk_index']}")
    print(f"title: {chunk['metadata']['section_title']}")
    print(f"section number: {chunk['metadata']['section_number']}")
    print("*" * 80)




