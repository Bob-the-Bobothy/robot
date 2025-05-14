from magicbot import AutonomousStateMachine, timed_state, state
from wpimath.units import *

from controllers.drive import Drive
from controllers.ball_shooter import BallShooter

class DriveAndShoot(AutonomousStateMachine):
    
    MODE_NAME = "Drive forward onto a ball and shoot"
    DEFAULT = False

    drive: Drive
    shooter: BallShooter

    drive_speed = 0.4

    @state()
    def running(self):
        self.next_state = "drive_forward"

    @timed_state(duration=1, first=True, next_state="shoot")
    def drive_forward(self):
        self.drive.drive("tank", -self.drive_speed, -self.drive_speed)

    @state(next_state="running")
    def shoot(self):
        self.shooter.fire()

    def on_disable(self):
        self.drive.stop()
        self.shooter.stop()
        


    



    