from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from document_processor import process_documents
from graph_generator import generate_graph

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
        selected_model = request.form.get('model', 'chatgpt')  # Get model selection
        uploaded_files = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(file_path)

        if not uploaded_files:
            return jsonify({'error': 'No valid PDF files uploaded'})

        # Process all uploaded documents
        results = process_documents(uploaded_files, selected_model)

        # Generate classification graph
        generate_graph(results)

        return jsonify({'documents': results})

    return render_template('upload.html')

@app.route('/graphs')
def show_graph():
    return render_template('graphs.html')

@app.route('/get_graph')
def get_graph():
    return send_file("static/classification_graph.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
