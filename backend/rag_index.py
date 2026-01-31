from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from db import cursor

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index():
    cursor.execute("SELECT text FROM posts")
    rows = cursor.fetchall()

    texts = [r[0] for r in rows]

    print(f"Embedding {len(texts)} posts...")

    embeddings = model.encode(texts, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    faiss.write_index(index, "rag.index")

    np.save("rag_texts.npy", np.array(texts))

    print("RAG index built successfully!")

if __name__ == "__main__":
    build_index()