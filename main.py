import threading
from flask import Flask, render_template

app = Flask(__name__, template_folder="static", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    server_thread = threading.Thread(target=app.run, args=("0.0.0.0",), kwargs={"debug": False})

    server_thread.start()