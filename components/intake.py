import magicbot
import wpilib

from util.helper_scripts import clamp


class Intake:
    intake_motor: wpilib.PWMVictorSPX
    
    intake_speed = magicbot.tunable(0.7)
    
    def __init__(self):
        self.enabled = False
    
    def enable(self, control=1):
        self.enabled = True
        self.control = control

    def execute(self):
        if self.enabled:
            self.intake_motor.set(self.intake_speed * self.control)
        else:
            self.intake_motor.set(0)

        self.enabled = False
