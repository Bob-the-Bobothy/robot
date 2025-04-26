import magicbot
import wpilib

from util.helper_scripts import clamp


class Hood:
    hood_motor: wpilib.PWMSparkMax
    
    hood_speed = magicbot.tunable(0.25)
    
    def __init__(self):
        self.enabled = False
    
    def rotate(self, control=0):
        self.enabled = True
        self.control = control

    def set_speed(self, new_value):
        self.hood_speed = clamp(new_value, 0, 1)
    
    def execute(self):
        if self.enabled:
            self.hood_motor.set(self.intake_speed * self.control)
        else:
            self.hood_motor.set(0)
            
        self.enabled = False