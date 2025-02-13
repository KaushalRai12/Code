from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from document_processor import process_documents

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('files')  # Get multiple files
        uploaded_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(file_path)

        if not uploaded_files:
            return jsonify({'error': 'No valid PDF files uploaded'})

        # Process documents
        results = process_documents(uploaded_files)

        return jsonify({'documents': results})

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
