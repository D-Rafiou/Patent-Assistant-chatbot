# this is where we make the chunks into normalized vectors


from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import pickle

data = "../output/output.json"
chunks = []

with open(data,"r") as file:
    chunks = json.load(file)
content = [chunk["content"] for chunk in chunks]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(content,show_progress_bar=True)

embeddings_np = np.array(embeddings).astype("float32")
faiss.normalize_L2(embeddings_np)
index = faiss.IndexFlatIP(embeddings_np.shape[1])
index.add(embeddings_np)
# we make dictionary that maps index to chunk 
chunk_map = {i:chunk for i,chunk in enumerate(chunks)}

with open("store/chunks_map.pkl","wb") as f:
    pickle.dump(chunk_map,f)

faiss.write_index(index,"store/my_index.faiss")




