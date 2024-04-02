from flask import Flask, request, send_file
import kickoff
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/process-receipts', methods=['POST'])
def process_receipts():
    # Get the uploaded image files
    uploaded_files = request.files.getlist('images')
    print(f"Received {len(uploaded_files)} files")
    # Call the existing functions from kickoff.py
    excel_data = kickoff.run(uploaded_files)

    # Return the generated Excel file data
    return excel_data, {'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Content-Disposition': 'attachment; filename=expense_tracker.xlsx'}