from serial import Serial


class ModifiedServoArray(): ## TODO: Rename to ContinousServoArray?
    """
    Array of continous servos. The speed of each servo is modified by setting the corresponding value in the self.speeds list.
    """

    def __init__(self, serial: Serial, indices = range(4)):
        self._indices = indices
        self._serial = serial
        self.count = len(indices)
        self.speeds = [0] * self.count
        self.offsets = [0] * self.count

    def stop_all(self):
        for i in self.count:
            self.speeds[i] = self.offsets[i]
    
    def update(self):
        # Create command to update all servos at once
        command = ""
        for i in range(self.count):
            speed = self.speeds[i] + self.offsets[i]
            command += f"#{self._indices[i]} P{speed}"
        command += "\r"

        self._serial.write(command.encode("ascii"))
