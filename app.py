from datetime import datetime
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

STORAGE_DIR = Path("storage")
DATA_FILE = STORAGE_DIR / "data.json"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form.get('username')
        message_text = request.form.get('message')

        if username and message_text:
            STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            
            data = {}
            if DATA_FILE.exists():
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

            timestamp = str(datetime.now())
            data[timestamp] = {
                "username": username,
                "message": message_text
            }

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))
    return render_template('message.html')


@app.route('/read')
def read_messages():
    messages = {}
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            messages = {}
            
    return render_template('read.html', messages=messages)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(port=3000, debug=True)