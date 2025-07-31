#This tool was created for personal research and educational purposes—not intended as professional legal advice.

# Patent-Assistant-chatbot

A chatbot that answers questions about the patent process using vector search and the Together AI API.

---

## 🔧 Project Structure

```plaintext
Patent-Assistant-chatbot/
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── chunks_to_vector.py
│ │ ├── pdf_to_chunks.py
│ │ └── store/
│ │ ├── index.faiss
│ │ └── chunk_map.json
│ ├── data/
│ │ └── [PDF files here]
│ ├── output/
│ │ └── output.json
│ └── requirements.txt
├── frontend/
│ └── my-react-app/
│ ├── public/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── App.css
│ │ └── ...
│ └── ...
└── README.txt

## 🧠 How It Works

- `pdf_to_chunks.py`: Converts all patent-related PDFs into chunks of text and saves them into `output/output.json`.
- `chunks_to_vector.py`: Converts the JSON chunks into vector embeddings and creates a FAISS index. The resulting `index.faiss` and `chunk_map.json` are saved in the `store` folder.
- `main.py`: Starts a FastAPI server, loads the index and chunk map, and exposes a GET endpoint to query relevant context chunks. These chunks are used to construct a prompt for Together AI, which returns a patent-related response.

---

## ▶️ Starting the Backend

cd backend
pip install -r requirements.txt
fastapi dev main.py


---

## 🌐 Starting the Frontend

cd frontend/my-react-app
npm install
npm run dev

A static React app using Vite. All main logic and styling is in `App.jsx` and `App.css`.

---

## 📸 Demo & Usage


- Add your own Together AI API key as a .env variale and access it in the main.py within the backend
- Clone this repo and run the backend and frontend locally.

---

## 🛠️ Technologies Used

- Backend: FastAPI, FAISS, Sentence Transformers, Python, pdfplumber, numpy
- Frontend: React, Vite, JavaScript, CSS
- APIs: Together AI API for natural language generation
- Others: Git, GitHub, npm, pip



