import openai
import os
import PyPDF2
import re
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI(api_key=api_key)

DOCUMENT_CATEGORIES = {
    "Identity Documents": ["Passport", "Drivers License", "National ID", "Social Security Card"],
    "Financial Documents": ["Bank Statement", "Salary Slip", "Tax Return", "Credit Card Statement"],
    "Utility Documents": ["Electricity Bill", "Gas Bill", "Internet Bill", "Water Bill"],
    "Legal Documents": ["Lease Agreement", "Employment Contract", "NDAs", "Court Orders"],
    "Property Documents": ["Title Deeds", "House Ownership Papers", "Mortgage Documents"],
    "Educational Documents": ["Transcripts", "Certificates", "Recommendation Letters"],
    "Medical Records": ["Prescriptions", "Diagnostic Reports", "Insurance Claims"],
    "Employment Documents": ["Resume", "Offer Letter", "Pay Stub", "Performance Reviews"],
    "Compliance Documents": ["Audit Reports", "Risk Assessments", "Certifications"],
    "Invoices and Receipts": ["Purchase Orders", "Payment Receipts", "Vendor Invoices"],
    "Insurance Documents": ["Policy Papers", "Claim Forms", "Premium Receipts"],
    "Travel Documents": ["Travel Itineraries", "Boarding Passes", "Hotel Bookings"],
    "Project Documents": ["Proposals", "Project Plans", "Reports", "Gantt Charts"],
    "Marketing Documents": ["Campaign Plans", "Customer Surveys", "Advertising Materials"]
}

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file"""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return ' '.join([page.extract_text() for page in reader.pages if page.extract_text()])

def analyze_document(text, model):
    """Uses AI model to analyze the document"""
    try:
        prompt = f"""
        You are an AI document classifier. Your task is to analyze the document text and classify it into one of the following categories:
        
        {", ".join(DOCUMENT_CATEGORIES.keys())}.
        
        1️⃣ **Classify** the document into the most appropriate category.
        2️⃣ **Estimate the confidence percentage** (between 50-100%) for this classification.
        3️⃣ **Summarize** the document in 25 words.

        **Format your response like this:**
        ```
        Category: [Category Name]
        Confidence: [Confidence %]
        Summary: [Summary in 25 words]
        ```

        **Document Text:** {text[:4000]}
        """

        if model == "chatgpt":
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a document classification assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        elif model in ["local_chatgpt", "local_deepseek"]:
            # Placeholder for local LLM implementation
            return "Local LLM processing not implemented yet."
    except Exception as e:
        return f"Error: {str(e)}"


def extract_category(analysis):
    """Extracts category safely from AI response"""
    for category, examples in DOCUMENT_CATEGORIES.items():
        if category in analysis:
            return category
    return "Other Documents"

def determine_sensitivity(text):
    """Determines document sensitivity based on its content"""
    contains_name = bool(re.search(r'\b(Name|Full Name|Applicant|Owner)\b', text, re.IGNORECASE))
    contains_address = bool(re.search(r'\b(Address|Street|City|State|Zip|Postal Code)\b', text, re.IGNORECASE))
    contains_ssn = bool(re.search(r'\b(SSN|Social Security Number|National ID)\b', text, re.IGNORECASE))

    if contains_name and contains_address and contains_ssn:
        return "Highly Confidential"
    elif contains_name and contains_address:
        return "Confidential"
    else:
        return "Non-Sensitive"

def compute_confidence(text, category):
    """Computes confidence score based on keyword matching"""
    keywords = DOCUMENT_CATEGORIES.get(category, [])
    matches = sum(1 for keyword in keywords if keyword.lower() in text.lower())
    return min(100, max(50, (matches / max(1, len(keywords))) * 100))  # Scale between 50-100%

def process_documents(file_paths, model):
    """Processes multiple PDFs and returns results in structured format"""
    results = []

    for file_path in file_paths:
        text = extract_text_from_pdf(file_path)
        analysis = analyze_document(text, model)
        category = extract_category(analysis)
        sensitivity = determine_sensitivity(text)
        confidence = round(compute_confidence(text, category), 2)
        summary = ' '.join(analysis.split()[:25])  # Limit summary to 25 words

        results.append({
            'document_name': os.path.basename(file_path),
            'document_type': category,
            'sensitive': sensitivity,
            'confidence': confidence,
            'summary': summary
        })

        os.remove(file_path)  # Cleanup processed files

    return results
