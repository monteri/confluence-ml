import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    print(pdf_path)
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


def is_pdf_empty(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        return len(pdf_reader.pages[0].extract_text()) < 100


def remove_empty_pdfs(directory):
    removed = 0
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)

            if is_pdf_empty(file_path):
                os.remove(file_path)
                removed += 1
                print(f"Removed empty PDF: {filename}")
    print(f'REMOVED: {removed}')

your_directory_path = '/Users/admin/Desktop/pets/confluence-gather-data/data'
remove_empty_pdfs(your_directory_path)