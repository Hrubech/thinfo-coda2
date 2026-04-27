from flask import Flask, request
import subprocess, pickle, base64

app = Flask(__name__)


@app.route('/ping')
def ping():
    host = request.args.get('host', '8.8.8.8')
    result = subprocess.run(f"ping -c 1 {host}", shell=True,
                            capture_output=True, text=True)
    return result.stdout


@app.route('/load')
def load_data():
    data = request.args.get('data')
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)


@app.route('/health')
def health():
    return {"status": "ok", "version": "1.0.0"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
