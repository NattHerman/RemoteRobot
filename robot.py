from servoarray import ModifiedServoArray


class Robot():
    """
    This robot expects the servo array to contain four servos and be ordered anti-clockwise starting at the front left wheel.
    """

    def __init__(self, servos: ModifiedServoArray):
        if servos.count != 4:
            raise ValueError("This robot expects an array of four servos. Because it has four wheels.")

        self._servos: ModifiedServoArray = servos
        self._top_speed: int = 750 # Not sure what this unit would be
        self._current_speed: int = 0

        self._top_turning_rate: int = 750
        self._current_turning_rate: int = 0

    def set_turning_rate(self, turning_rate):
        """Set the current turning speed directly, absolute value of turning rate is limited to less than maximum turning speed."""

        self._current_turning_rate = max(-self._top_turning_rate, min(self._top_turning_rate, turning_rate))
        self.update()
    
    def set_normalized_turning_rate(self, normalized_turning_rate):
        """Set current turning speed, but normalized. Takes in a value from -1 to 1."""

        self._current_turning_rate = max(-1, min(1, normalized_turning_rate)) * self._top_turning_rate
        self.update()
    
    def set_speed(self, speed):
        """Set the current speed directly, absolute value of speed is limited to less than top speed."""

        self._current_speed = max(-self._top_speed, min(self._top_speed, speed))
        self.update()
    
    ## Set current speed, but normalized. Takes in a value from -1 to 1.
    def set_normalized_speed(self, normalized_speed):
        """Set current speed, but normalized. Takes in a value from -1 to 1."""
        
        self._current_speed = max(-1, min(1, normalized_speed)) * self._top_speed
        self.update()

    def update(self):
        """Update speed of motors."""

        if self._current_turning_rate == 0:
            # There is no turning, all wheels should be spinning at the same speed.
            # Remember, wheels are rotated 180 degrees on the other side of the vehicle.
            # We compensate by spinning those wheels the other way.
            self._servos.speeds[0] = self._current_speed
            self._servos.speeds[1] = self._current_speed
            self._servos.speeds[2] = -self._current_speed
            self._servos.speeds[3] = -self._current_speed

        elif self._current_speed == 0:
            # There is no forward movement, left wheels should spin in opposite direction to the right wheels.
            self._servos.speeds[0] = -self._current_turning_rate
            self._servos.speeds[1] = -self._current_turning_rate
            self._servos.speeds[2] = -self._current_turning_rate
            self._servos.speeds[3] = -self._current_turning_rate
        else:
            self._servos.speeds[0] =  self._current_speed - self._current_turning_rate
            self._servos.speeds[1] =  self._current_speed - self._current_turning_rate
            self._servos.speeds[2] = -self._current_speed - self._current_turning_rate
            self._servos.speeds[3] = -self._current_speed - self._current_turning_rate
        
        self._servos.update()            
