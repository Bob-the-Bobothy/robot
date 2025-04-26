import wpilib
import magicbot

class Shooter:
    shooter_motor: wpilib.PWMSparkMax

    # speed is tunable via NetworkTables
    shoot_speed = magicbot.tunable(1.0)

    def __init__(self):
        self.enabled = False

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def execute(self):
        '''This gets called at the end of the control loop'''
        if self.enabled:
            self.shooter_motor.set(self.shoot_speed)
        else:
            self.shooter_motor.set(0)

        self.enabled = False