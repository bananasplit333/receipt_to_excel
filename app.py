import tempfile
from flask import Flask, request, send_file
import kickoff
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process-receipts', methods=['POST', 'OPTIONS'])
def process_receipts():
    if request.method == 'OPTIONS':
        # Preflight request. Reply successfully:
        response = app.response_class(
            response='',
            status=200,
            mimetype='application/json'
        )
        return response

    # Get the uploaded image files
    uploaded_files = request.files.getlist('images')
    print(f"Received {len(uploaded_files)} files")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        temp_file_path = temp_file.name

        # Call the existing functions from kickoff.py
        kickoff.run(uploaded_files, temp_file_path)

        # Send the file
        response = send_file(temp_file_path, as_attachment=True, download_name='expense_tracker.xlsx')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

if __name__ == '__main__':
    app.run(debug=True)