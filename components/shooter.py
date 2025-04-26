import magicbot
import wpilib

from util.helper_scripts import clamp


class Shooter:
    shooter_motor: wpilib.PWMSparkMax

    # speed is tunable via NetworkTables
    shoot_speed = magicbot.tunable(1.0)

    def __init__(self):
        self.enabled = False

    def enable(self, control=1):
        '''Causes the shooter motor to spin'''
        self.enabled = True
        self.control = control

    def set_speed(self, new_value):
        self.shoot_speed = clamp(new_value, 0, 1)

    def execute(self):
        '''This gets called at the end of the control loop'''
        if self.enabled:
            self.shooter_motor.set(self.shoot_speed * self.control)
        else:
            self.shooter_motor.set(0)

        self.enabled = False