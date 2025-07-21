import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="static", static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", debug=True)