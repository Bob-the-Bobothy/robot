from magicbot import AutonomousStateMachine, timed_state, state

from controllers.drive import Drive
from controllers.ball_shooter import BallShooter

class DriveAndShoot(AutonomousStateMachine):
    
    MODE_NAME = "Drive and Shoot"
    DEFAULT = False

    drive: Drive
    ball_shooter: BallShooter

    drive_speed = 0.4

    @state(first=True)
    def ready(self):
        self.drive.drive_speed = 1
        self.next_state("prime_shooting")
    
    @timed_state(duration=1.5, next_state="shoot")
    def prime_shooting(self):
        self.ball_shooter.control(shooter=1)

    @timed_state(must_finish=True, duration=2.0, next_state="stop")
    def shoot(self):
        self.drive.drive("tank", -self.drive_speed, -self.drive_speed)
        self.ball_shooter.control(shooter=1, intake=1)
    
    @state
    def stop(self):
        self.drive.stop()
        self.ball_shooter.stop()
        super().done()
