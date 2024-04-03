import tempfile
from flask import Flask, request, send_file
import kickoff
from flask_cors import cross_origin, CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin and origin.startswith('https://drag-and-drop-nextjs-bntiql1xb-bananasplit333s-projects.vercel.app/'):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/process-receipts', methods=['POST'])
def process_receipts():
    # Get the uploaded image files
    uploaded_files = request.files.getlist('images')
    print(f"Received {len(uploaded_files)} files")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        temp_file_path = temp_file.name

        # Call the existing functions from kickoff.py
        kickoff.run(uploaded_files, temp_file_path)

        # Send the file
        return send_file(temp_file_path, as_attachment=True, download_name='expense_tracker.xlsx')

if __name__ == '__main__':
    app.run(debug=True)