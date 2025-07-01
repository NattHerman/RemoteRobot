from serial import Serial
from time import sleep

def test(serial_path):
    print("Testing", serial_path)
    port = Serial(serial_path, baudrate=9600)

    for i in range(25):
        b = bytes([255, 0, i * 10])
        port.write(b)
        print(f"Wrote bytes: {b}")
        sleep(0.1)

test("/dev/ttyS0")
test("/dev/serial0")