import openai
import os
import PyPDF2
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI(api_key=api_key)

def extract_text_from_pdf(file_path):
    """ Extracts text from a PDF file """
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return ' '.join([page.extract_text() for page in reader.pages if page.extract_text()])

def analyze_document(text):
    """ Sends extracted text to GPT for analysis """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a document categorization assistant. Identify the category of the document and summarize it."},
                {"role": "user", "content": f"Categorize and summarize this document:\n\n{text[:4000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def extract_category(analysis):
    """ Extracts category safely from GPT response """
    try:
        if "Category:" in analysis:
            category_line = analysis.split("Category:")[1].strip().split("\n")[0]
            return category_line.strip()
        return "Unknown Category"
    except Exception:
        return "Unknown Category"

def process_documents(file_paths):
    """ Processes multiple PDFs and returns results in structured format """
    results = []

    for file_path in file_paths:
        text = extract_text_from_pdf(file_path)
        analysis = analyze_document(text)

        category = extract_category(analysis)  # Use safe extraction method

        results.append({
            'document_name': os.path.basename(file_path),
            'category': category,
            'summary': analysis[:500]  # Limit summary to 500 characters
        })

        os.remove(file_path)  # Cleanup processed files

    return results
