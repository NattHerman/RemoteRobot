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
serial_available = False

# We still want the server to boot up even if the serial port is unavailable.
try:
    SSC32 = Serial(SSC32_port_path, 115_200)
    serial_available = True
except:
    print(f"WARNING: Serial port '{SSC32_port_path}' is unavailable")
    SSC32 = Serial()
    serial_available = False

servo_offsets_dump_path = r"robot/pickles/servo_offsets.pkl"

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
        # If the pickle cant be unpickled, delete the pickle and move on.
        try:
            # Load/unpickle offsets from file
            with open(servo_offsets_dump_path, "br") as file:
                servo_array.offsets = pickle.load(file)
        except pickle.UnpicklingError:
            print(f"ERROR: Servo offset pickle at '{servo_offsets_dump_path}' cannot be unpickled")
            print(f"Deleting file at '{servo_offsets_dump_path}'")
            os.remove(servo_offsets_dump_path)


@app.route("/")
def index():
    return render_template("index.html")

# Recieve robot's new motion state
@socketio.event
def robot_update(speed, turning):
    # Update movement state of robot
    print('set state:', speed, turning)
    if serial_available:
        robot.set_normalized_speed(speed)
        robot.set_normalized_turning_rate(turning)

@socketio.event
def set_offsets(offsets):
    print(offsets)
    # Clamp offsets to [-1500, 1500]
    for i in range(servo_array.count):
        offsets[i] = min(1500, max(-1500, offsets[i]))
    
    servo_array.offsets = offsets
    save_offsets(servo_array)

# When a client disconnects stop the robot.
@socketio.on('disconnect')
def test_disconnect(reason):
    ## Halt robot
    if serial_available:
        robot.set_normalized_speed(0)
        robot.set_normalized_turning_rate(0)


if __name__ == "__main__":
    print("Loading offsets")
    load_offsets(servo_array)

    print("Starting web server")
    socketio.run(app, "0.0.0.0", debug=True)
