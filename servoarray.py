from serial import Serial

class ModifiedServoArray():
    def __init__(self, serial, indices = range(4)):
        self._indices = indices
        self._serial = serial
        self.length = len(indices)
        self.speeds = [0] * self.length
        self.offsets = [0] * self.length

    def stop_all(self):
        for i in self.length:
            self.speeds[i] = self.offsets[i]
    
    def update(self):
        command = ""
        for i in range(self.length):
            speed = self.speeds[i] + self.offsets[i]
            command += f"#{self._indices[i]} P{speed}"
        command += "\r"
        self._serial.write(command.encode("ascii"))