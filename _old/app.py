from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename
from io import StringIO, BytesIO
import zipfile
import numpy as np  # ← ADD THIS IMPORT

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Add this function to convert numpy/pandas types to Python native types
def convert_to_python_type(obj):
    """Convert numpy/pandas types to Python native types"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_python_type(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_python_type(item) for item in obj]
    return obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Handle multiple CSV files upload and processing"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')  # Get multiple files
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    try:
       
        results_df=[] # dummy
        
        """
        #process data to df
        results_df = data_processing(conversion_type, file_path)
        """
        #create string to download
        csv_string = results_df.to_csv(index=False)

        # Response for later including download
        response_data = {
            'total_combined_records': int(len(results_df)),  # ← CONVERT HERE
            'csv_data': csv_string,
            'success': True
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

@app.route('/download', methods=['POST'])
def download():
    """Download the processed data as CSV"""
    try:
        data = request.get_json()
        csv_data = data.get('csv_data')
        
        if not csv_data:
            return jsonify({'error': 'No data to download'}), 400
        
        # Convert string to bytes
        csv_bytes = BytesIO(csv_data.encode('utf-8'))
        
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name='analysis_results.csv'
        )
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File is too large (max 16MB)'}), 413

if __name__ == "__main__":
    app.run(debug=True, port=5000)