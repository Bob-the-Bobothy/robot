from magicbot import AutonomousStateMachine, timed_state, state
import wpilib
import math
from wpimath.units import *

from components.drivetrain import Drivetrain
from util.constants import Constants

class Square(AutonomousStateMachine):
    
    MODE_NAME = "Drive in a Square"
    DEFAULT = True

    drivetrain: Drivetrain

    const = Constants()

    drive_speed = 0.4 # % of top speed

    side_length: meters = 4 #meters
    turn_angle: degrees = 90 #degrees

    drive_time = side_length / const.TOP_SPEED / drive_speed
    turn_time = math.pi * const.WHEELBASE * (turn_angle / 360) / drive_speed

    modified_top_speed = const.TOP_SPEED * drive_speed

    @state
    def running(self):
        repetitions = 4
        while repetitions > 0:
            self.next_state("drive_forward")

            repetitions -= 1

    @timed_state(duration=drive_time, first=True, next_state="turn")
    def drive_forward(self):
        self.drivetrain.autoDrive(self.modified_top_speed, self.modified_top_speed)

    @timed_state(duration=turn_time, next_state="running")
    def turn(self):
        self.drivetrain.autoDrive(-self.modified_top_speed, self.modified_top_speed)
        


    



    