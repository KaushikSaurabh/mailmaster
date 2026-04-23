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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    thread = threading.Thread(target=run_validation_task, args=(filepath,))
    thread.start()
    return jsonify({'status': 'started'})

def run_validation_task(filepath):
    try:
        socketio.emit('log_message', {'msg': f'[*] Starting validation for {os.path.basename(filepath)}'})
        run_pro_validation(filepath)
        socketio.emit('log_message', {'msg': '[SUCCESS] Validation complete!'})
        socketio.emit('progress', {'percent': 100})
        # Note: In a real app we'd pass the actual clean list path back
    except Exception as e:
        socketio.emit('log_message', {'msg': f'[!] Error: {str(e)}'})

@app.route('/api/verify-smtp', methods=['POST'])
def verify_smtp():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    thread = threading.Thread(target=run_smtp_task, args=(filepath,))
    thread.start()
    return jsonify({'status': 'started'})

def run_smtp_task(filepath):
    try:
        socketio.emit('smtp_log', {'msg': f'[*] Verifying SMTPs in {os.path.basename(filepath)}...'})
        checker_path = os.path.join("core", "smtp_checker.py")
        
        # We run the checker and capture output
        process = subprocess.Popen(
            [sys.executable, checker_path, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        for line in process.stdout:
            socketio.emit('smtp_log', {'msg': line.strip()})
        
        process.wait()
        socketio.emit('smtp_log', {'msg': '[SUCCESS] SMTP Verification complete!'})
        socketio.emit('smtp_progress', {'percent': 100})
    except Exception as e:
        socketio.emit('smtp_log', {'msg': f'[!] Error: {str(e)}'})

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
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
