from serial import Serial
from time import sleep

def test(serial_path):
    print("Testing", serial_path)
    port = Serial(serial_path, baudrate=115_200)

    port.write(b"#0 P1500 S750 \x13")

test("/dev/ttyS0")
#test("/dev/serial0")