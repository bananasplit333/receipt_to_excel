import tempfile
from flask import Flask, request, send_file, jsonify
import kickoff
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process-receipts', methods=['POST'])
def process_receipts():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)