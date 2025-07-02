from serial import Serial
from time import sleep

def test(serial_path):
    print("Testing", serial_path)
    port = Serial(serial_path, baudrate=115_200)
    
    b = "#0 P1500 S750 <cr>".encode("ascii")
    port.write(b)
    print(b)

test("/dev/ttyS0")
test("/dev/serial0")
