import wpilib
import magicbot

class Hood:
    hood_motor: wpilib.PWMSparkMax
    
    hood_speed = magicbot.tunable(0.25)
    
    def __init__(self):
        self.enabled = False
    
    def rotate(self, control=0):
        self.enabled = True
        self.control = control
    
    def execute(self):
        if self.enabled:
            self.hood_motor.set(self.intake_speed * self.control)
        else:
            self.hood_motor.set(0)
            
        self.enabled = False