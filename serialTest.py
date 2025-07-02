from serial import Serial
from time import sleep

def debug_write(port, string):
    port.write(string)
    print(string)


def test(serial_path):
    print("Testing", serial_path)
    port = Serial(serial_path, baudrate=115_200)
    
    debug_write(port, b"#1 P1500 T100 \r")
    sleep(0.1)
    debug_write(port, b"#1 P700 T100 \r")

test("/dev/ttyS0")
#test("/dev/serial0")
