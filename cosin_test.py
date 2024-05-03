import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load the model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Load the Faiss index
index = faiss.read_index("pdf_embeddings.index")

# Load PDF paths (Assuming you saved this during preprocessing)
with open('pdf_data.pickle', 'rb') as f:
    pdf_data = pickle.load(f)

def search_pdfs(query_text):
    # expanded_query = expand_query(query_text)  # Expand first
    print('query_text', query_text)
    query_embedding = model.encode(query_text).reshape(1, -1)
    distances, indices = index.search(query_embedding, k=10)

    for distance, index_id in zip(distances[0], indices[0]):
        pdf_path = pdf_data[index_id]
        # Assuming you know the original segment indexing of each PDF
        segment_index = index_id
        print(f"PDF: {pdf_path}, Segment Index: {segment_index}, Distance: {distance}")

if __name__ == "__main__":
    query_text = input("Enter your search query: ")
    search_pdfs(query_text)
