from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
import os

app = Flask(__name__)

DATA_FILE = "storage/data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")

        data = load_data()

        timestamp = str(datetime.now())
        data[timestamp] = {
            "username": username,
            "message": message
        }

        save_data(data)

        return redirect("/")

    return render_template("message.html")


@app.route("/read")
def read():
    messages = load_data()
    return render_template("read.html", messages=messages)


@app.errorhandler(404)
def error(e):
    return render_template("error.html"), 404


if __name__ == "__main__":
    os.makedirs("storage", exist_ok=True)
    app.run(host="0.0.0.0", port=3000)
    