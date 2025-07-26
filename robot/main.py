# Web server modules
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

# Robot control modules
from serial import Serial
from robotlib import Robot
from servoarray import ModifiedServoArray


app = Flask(__name__, template_folder="../static", static_folder="../static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

serial_port_path = "/dev/ttyS0"

try:
    port = Serial(serial_port_path, 115_200)
except:
    print(f"WARNING: Serial port '{serial_port_path}' is unavailable")
    port = Serial()

servo_array = ModifiedServoArray(port, [1, 2, 3, 4])
servo_array.offsets = [0, 0, 0, 0]
robot = Robot(servo_array)


@app.route("/")
def index():
    return render_template("index.html")

@socketio.event
def robot_update(speed, turning):
    # Update movement state of robot
    print('received args:', speed, turning)
    robot.set_normalized_speed(speed)
    robot.set_normalized_turning_rate(turning)

@socketio.on('disconnect')
def test_disconnect(reason):
    ## Halt robot
    pass

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", debug=True)
