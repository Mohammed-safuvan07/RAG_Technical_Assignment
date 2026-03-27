from PyPDF2 import PdfReader
from docx import Document


# Function to read PDF files and extract text from each page
def read_pdf(file):
    docs = []
    pdf = PdfReader(file)

    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        docs.append({
            "text": text,
            "metadata": {
                "source": file.name,
                "page": i + 1
            }
        })
    return docs

# Function to read DOCX files and extract text from paragraphs
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read TXT files
def read_txt(file):
    return file.read().decode("utf-8")


def load_documents(files):
    all_docs = []

    for file in files:
        if file.name.endswith(".pdf"):
            all_docs.extend(read_pdf(file))  # returns docs with metadata

        elif file.name.endswith(".docx"):
            text = read_docx(file)
            all_docs.append({
                "text": text,
                "metadata": {
                    "source": file.name,
                    "page": "N/A"
                }
            })

        elif file.name.endswith(".txt"):
            text = read_txt(file)
            all_docs.append({
                "text": text,
                "metadata": {
                    "source": file.name,
                    "page": "N/A"
                }
            })

    return all_docs
