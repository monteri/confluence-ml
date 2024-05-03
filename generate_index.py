import os
import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def extract_text_from_pdf(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    pdf_file.close()
    return text

def segment_text(text, segment_size=5):  # Around 500 words per segment
    words = text.split()
    segments = []
    current_segment = ""

    for word in words:
        if len(current_segment.split()) >= segment_size:
            segments.append(current_segment)
            current_segment = ""
        current_segment += word + " "

    if current_segment:
        segments.append(current_segment)

    return segments

def preprocess_pdfs(data_dir):
    embeddings = []
    pdf_data = []  # Store pdf_path and index
    c = 0
    files = os.listdir(data_dir)
    for file in files[:1000]:
        if file.endswith(".pdf"):
            c += 1
            pdf_path = os.path.join(data_dir, file)

            text = extract_text_from_pdf(pdf_path)
            segments = segment_text(text)
            print(f'{c} / {len(files)}')
            segment_embeddings = model.encode(segments)

            for i, embedding in enumerate(segment_embeddings):
                embeddings.append(embedding)
                pdf_data.append((pdf_path, i))  # Store path and segment index

    return np.array(embeddings), pdf_data

def build_faiss_index(embeddings):
    d = embeddings.shape[1]  # Embedding dimensionality
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

def save_index(index, index_path):
    faiss.write_index(index, index_path)

# Preprocessing
embeddings, pdf_data = preprocess_pdfs("./less_data")
index = build_faiss_index(embeddings)
print('pdf_data', pdf_data)
with open('pdf_data.pickle', 'wb') as f:
    pickle.dump(pdf_data, f)
save_index(index, "pdf_embeddings.index")  # Save for future use
