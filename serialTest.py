from serial import Serial
from time import sleep

print("Testing '/dev/ttyS0'")
port = Serial("/dev/ttyS0", baudrate=9600)

for i in range(25):
    b = [255, 0, i * 10]
    port.write(bytes(b))
    print(f"Wrote bytes: {b}")
    sleep(0.1)

print("Testing '/dev/serial0'")
port = Serial("/dev/serial0", baudrate=9600)

for i in range(25):
    b = [255, 0, i * 10]
    port.write(bytes(b))
    print(f"Wrote bytes: {b}")
    sleep(0.1)