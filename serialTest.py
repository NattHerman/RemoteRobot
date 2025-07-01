from serial import Serial

port = Serial("serial0", baudrate=9600)

port.write(bytes([255, 0, 100]))