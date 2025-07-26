import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="../static", static_folder="../static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@socketio.event
def robot_update(speed, turning):
    # Update movement state of robot
    print('received args:', speed, turning)

@socketio.on('disconnect')
def test_disconnect(reason):
    ## Halt robot
    pass

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", debug=True)
