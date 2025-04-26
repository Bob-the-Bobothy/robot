import wpilib
import magicbot

class Intake:
    intake_motor: wpilib.PWMVictorSPX
    
    intake_speed = magicbot.tunable(0.7)
    
    def __init__(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True
    
    def execute(self):
        if self.enabled:
            self.intake_motor.set(self.intake_speed)
        else:
            self.intake_motor.set(0)

        self.enabled = False
