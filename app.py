from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_son.log')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_agent():
    subprocess.Popen(['python', 'main.py', 'start'])
    return jsonify(status='ok')

@app.route('/stop', methods=['POST'])
def stop_agent():
    subprocess.Popen(['python', 'main.py', 'stop'])
    return jsonify(status='ok')

@app.route('/command', methods=['POST'])
def send_command():
    command = request.json.get('command')
    if command:
        subprocess.Popen(['python', 'c2.py'] + command.split())
        return jsonify(status='ok')
    return jsonify(status='error', message='No command provided'), 400

@app.route('/log')
def get_log():
    if not os.path.exists(LOG_FILE):
        return ''
    with open(LOG_FILE, 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
