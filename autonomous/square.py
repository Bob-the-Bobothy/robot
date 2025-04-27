from magicbot import AutonomousStateMachine, timed_state, state
import wpilib
import math
from wpimath.units import *

from controllers.drive import Drive
from util.constants import Constants

class Square(AutonomousStateMachine):
    
    MODE_NAME = "Drive in a Square"
    DEFAULT = False

    drive: Drive

    const = Constants()
    drive_speed = 0.4

    side_length: meters = 4 #meters
    turn_angle: degrees = 90 #degrees

    drive_time = side_length / const.TOP_SPEED / drive_speed
    turn_time = math.pi * const.WHEELBASE * (turn_angle / 360) / drive_speed

    @state
    def running(self):
        old_speed = self.drive.drive_speed
        self.drive.drive_speed = self.drive_speed

        repetitions = 4
        while repetitions > 0:
            self.next_state("drive_forward")

            repetitions -= 1

        self.drive.drive_speed = old_speed
        

    @timed_state(duration=drive_time, first=True, next_state="turn")
    def drive_forward(self):
        self.drive.drive("tank", -self.drive_speed, -self.drive_speed)

    @timed_state(duration=turn_time, next_state="running")
    def turn(self):
        self.drive.drive("tank", self.drive_speed, -self.drive_speed)

    def on_disable(self):
        self.drive.stop()
        


    



    