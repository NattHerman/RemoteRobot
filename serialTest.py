from serial import Serial

port = Serial("/dev/ttyS0", baudrate=9600)

port.write(bytes([255, 0, 0]))
