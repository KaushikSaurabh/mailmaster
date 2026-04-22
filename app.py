from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
import threading
import subprocess
import sys
from excel_processor import run_pro_validation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mailmaster_secret'
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/validate', methods=['POST'])
def validate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Run validation in a background thread to keep UI responsive
    thread = threading.Thread(target=run_validation_task, args=(filepath,))
    thread.start()
    
    return jsonify({'status': 'started', 'filename': filename})

def run_validation_task(filepath):
    try:
        socketio.emit('log_message', {'msg': f'[*] Starting validation for {os.path.basename(filepath)}'})
        
        # We wrap the existing logic but redirect output to socket
        # Note: In a production app, we'd capture stdout line-by-line
        run_pro_validation(filepath)
        
        socketio.emit('log_message', {'msg': '[SUCCESS] Validation complete!'})
        socketio.emit('progress', {'percent': 100})
    except Exception as e:
        socketio.emit('log_message', {'msg': f'[!] Error: {str(e)}'})

@app.route('/api/scan', methods=['POST'])
def scan_content():
    content = request.json.get('content')
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_template.html')
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    scanner_bin = os.path.join("core", "spamscanner.exe")
    if os.path.exists(scanner_bin):
        result = subprocess.run([scanner_bin, "scan", temp_path], capture_output=True, text=True)
        return jsonify({'result': result.stdout})
    else:
        return jsonify({'error': 'Scanner binary missing'}), 500

if __name__ == '__main__':
    print("[*] MailMaster UI running at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
