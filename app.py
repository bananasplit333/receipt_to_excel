import tempfile
from flask import Flask, render_template_string, request, send_file, jsonify
import kickoff
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    message = 'Welcome to the Receipt Processing API'
    return render_template_string(f"""
        <html>
            <head>
                <title>Receipt Processing API</title>
            </head>
            <body>
                <h1>{message}</h1>
                <p>JSON Response: {{{{ message | tojson }}}}</p>
            </body>
        </html>
    """, message=message)


@app.route('/test')
def test_endpoint():
    return jsonify({'message': 'Test endpoint is working'})

@app.route('/process-receipts', methods=['POST'])
def process_receipts():
    try:
        # Get the uploaded image files
        uploaded_files = request.files.get('image')   
        print(f"Received {(uploaded_files)}")
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_file_path = temp_file.name
            # Call the existing functions from kickoff.py
            json_response = kickoff.run(uploaded_files, temp_file_path)

            #send back json file 
            return jsonify(json_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
