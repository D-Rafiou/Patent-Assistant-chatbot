import faiss
import pickle



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