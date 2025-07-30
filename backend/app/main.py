import faiss
from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv
from together import Together
import pickle
load_dotenv
from typing import Union

from fastapi import FastAPI
app = FastAPI()

index = faiss.read_index("./store/my_index.faiss")

with open("./store/chunks_map.pkl", "rb") as f:
    chunk_map = pickle.load(f)

def clean_response(raw_text: str) -> str:
    # Remove <think>...</think> block
    if "<think>" in raw_text and "</think>" in raw_text:
        raw_text = raw_text.split("</think>")[-1]
    
    # Replace \n with space
    cleaned_text = raw_text.replace("\\n", " ").strip()
    
    # Optional: collapse multiple spaces
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text
client = Together(api_key="499314ef838bf53afd2b502d4e78c01551edd0028219be7b6f12f166341f0947") # auth defaults to os.environ.get("TOGETHER_API_KEY")

@app.get("/question/{query}")
def answerUser(query:str):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_vec  =  model.encode([query],show_progress_bar=True)
    faiss.normalize_L2(query_vec)
    k = 5
    distances,indices =  index.search(query_vec,k)
    context = "\n\n".join(
    chunk_map[idx]["content"] for idx in indices[0]
)
    prompt = f"""You are an AI legal assistant with expert knowledge of United States patent law and the USPTO (United States Patent and Trademark Office).  
    Use the following context **internally** to answer the user's question, but **do not mention the context, its existence, or that you used it** in your response.  
    Respond as if the knowledge is your own and part of your general expertise.  
    If the context does not fully answer the question, use your own legal knowledge to fill in any gaps as needed. Do not show your thinking answer directly

    Context: {context}  
    Question: {query}"""
    response =  client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Thinking-2507",
    messages=[
      {
        "role": "user",
        "content": prompt
                    }
    ]
)
    return {clean_response(response.choices[0].message.content)}




