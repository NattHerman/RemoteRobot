from serial import Serial


class MiniSSCIIServo():
    def __init__(self, servo_index: int, serial_port: Serial):
        self._index = servo_index
        self._port = serial_port


    ## speed must be an int in the range [-127, 127] (inclusive).
    def set_speed(self, speed: int):
        pass
