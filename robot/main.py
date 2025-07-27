# Web server modules
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

# Robot control modules
from serial import Serial
from robotlib import Robot
from servoarray import ModifiedServoArray

import pickle
import os


# Initialize Flask server with SocketIO
app = Flask(__name__, template_folder="../static", static_folder="../static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# The path of a serial port where an SSC32 servo controller can be accessed.
SSC32_port_path = "/dev/ttyS0"

# We still want the server to boot up even if the serial port is unavailable.
try:
    SSC32 = Serial(SSC32_port_path, 115_200)
except:
    print(f"WARNING: Serial port '{SSC32_port_path}' is unavailable")
    SSC32 = Serial()

servo_offsets_dump_path = "pickles/servo_offsets.pkl"

# Initialize servo array and robot
servo_array = ModifiedServoArray(SSC32, [1, 2, 3, 4])
servo_array.offsets = [0, 0, 0, 0]
robot = Robot(servo_array)


# Save and load servo offsets
def save_offsets(servo_array: ModifiedServoArray):
    # Dump/pickle offsets to file
    with open(servo_offsets_dump_path, "bw") as file:
        pickle.dump(servo_array.offsets, file)

def load_offsets(servo_array: ModifiedServoArray):
    # Check if file exists
    if os.path.exists(servo_offsets_dump_path):
        # Load/unpickle offsets from file
        with open(servo_offsets_dump_path, "br") as file:
            servo_array.offsets = pickle.load(file)


@app.route("/")
def index():
    return render_template("index.html")

# Recieve robot's new motion state
@socketio.event
def robot_update(speed, turning):
    # Update movement state of robot
    print('received args:', speed, turning)
    robot.set_normalized_speed(speed)
    robot.set_normalized_turning_rate(turning)

# When a client disconnects, we want the robot to stop.
@socketio.on('disconnect')
def test_disconnect(reason):
    ## Halt robot
    robot.set_normalized_speed(0)
    robot.set_normalized_turning_rate(0)

# TODO: remove this event, here and client-side
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", debug=True)
