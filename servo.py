from serial import Serial


class SSC32ModifiedServo():
    def __init__(self, servo_index: int, SSC32_port: Serial):
        self._index = servo_index
        self._ser = SSC32_port

        ## Offset where servo is still, in microseconds.
        self.offset = 0

    def set_speed(self, speed: int, ):
        position = 1500 + speed + self.offset
        string = f"#{self._index} P{position} \r"
        self._ser.write(string.encode("ascii"))


if __name__ == "__main__":
    SSC32 = Serial("/dev/ttyS0", 115_200)

    servo_wheel = SSC32ModifiedServo(0, SSC32)

    speed = int(input("Servo speed:"))
    servo_wheel.set_speed(speed)