"""
AI Foundations: 10.3 RAG, Embeddings, and Vector Search

This script implements a Retrieval-Augmented Generation (RAG) pipeline
from scratch, explaining the math behind vector search.

CORE CONCEPTS:
1. RAG: Adding external data to an LLM's prompt to improve accuracy.
2. Embeddings: Converting text into high-dimensional numerical vectors.
   - Similar meanings = Vectors that are close together in space.
3. Vector Database: A system that stores embeddings and performs 'similarity search'.

THE MATH: COSINE SIMILARITY
To find how similar two vectors (A and B) are, we calculate the cosine of the
angle between them.

Formula: cos(theta) = (A . B) / (||A|| * ||B||)

Where:
- A . B is the dot product (sum of element-wise multiplications).
- ||A|| is the magnitude (length) of the vector.
- 1.0 = Identical direction, 0.0 = Orthogonal (unrelated), -1.0 = Opposite.
"""

import numpy as np

# --- 1. MOCK DATA (Our "Knowledge Base") ---
DOCUMENTS = [
    "The capital of France is Paris. It is known for the Eiffel Tower.",
    "The capital of Japan is Tokyo. It is famous for its technology and sushi.",
    "The capital of Canada is Ottawa. It is located in the province of Ontario.",
    "The capital of Australia is Canberra. It was chosen as a compromise between Sydney and Melbourne.",
]


# --- 2. MOCK EMBEDDING FUNCTION ---
def get_embedding(text):
    """
    In reality, you would use models like 'text-embedding-3-small' or HuggingFace.
    Here, we generate a mock 4-dimensional vector based on word presence.
    """
    text = text.lower()
    vector = np.zeros(4)
    if "france" in text or "paris" in text:
        vector[0] = 1.0
    if "japan" in text or "tokyo" in text:
        vector[1] = 1.0
    if "canada" in text or "ottawa" in text:
        vector[2] = 1.0
    if "australia" in text or "canberra" in text:
        vector[3] = 1.0

    # Add some 'noise' or 'semantic depth'
    vector += np.random.normal(0, 0.1, 4)

    # Normalize the vector (Magnitude = 1.0)
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 0 else vector


# --- 3. THE VECTOR DATABASE (Implementation) ---
class SimpleVectorDB:
    def __init__(self):
        self.vectors = []
        self.metadata = []

    def add_document(self, text):
        vector = get_embedding(text)
        self.vectors.append(vector)
        self.metadata.append(text)

    def search(self, query, top_k=1):
        query_vector = get_embedding(query)

        # Calculate Cosine Similarity for every document
        similarities = []
        for doc_vector in self.vectors:
            # Formula: (A . B) / (||A|| * ||B||)
            # Since our vectors are already normalized (norm=1), it's just the dot product!
            similarity = np.dot(query_vector, doc_vector)
            similarities.append(similarity)

        # Get indices of top_k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({"document": self.metadata[idx], "score": similarities[idx]})
        return results


# --- 4. THE RAG PIPELINE ---
def run_rag_pipeline(query):
    print(f"--- RAG PIPELINE ---")
    print(f"User Query: {query}")

    # 1. Setup DB
    db = SimpleVectorDB()
    for doc in DOCUMENTS:
        db.add_document(doc)

    # 2. RETRIEVE: Find relevant context
    results = db.search(query, top_k=1)
    context = results[0]["document"]
    score = results[0]["score"]

    print(f"Retrieved Context: {context} (Score: {score:.4f})")

    # 3. AUGMENT: Create the prompt
    rag_prompt = f"""
    Answer the question using only the context provided below.
    Context: {context}

    Question: {query}
    Answer:
    """

    print("\n--- AUGMENTED PROMPT ---")
    print(rag_prompt)

    # 4. GENERATE: (Simulated LLM)
    print("--- GENERATED ANSWER ---")
    if "Japan" in query:
        print("The capital of Japan is Tokyo, known for sushi and technology.")
    else:
        print("The answer is contained in the context above.")


if __name__ == "__main__":
    run_rag_pipeline("What is the capital of Japan?")
