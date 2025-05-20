from magicbot import StateMachine, state, timed_state

from components.shooter import Shooter
from components.hood import Hood
from components.intake import Intake

class BallShooter:
    shooter: Shooter
    intake: Intake
    hood: Hood

    def __init__(self):
        self.enabled = False

    def control(self, **kwargs):
        """Control the ball shooter and hood based on inputs.

        Args:
            inputs (dict): Dictionary containing control inputs.
        """
        self.output = kwargs

        self.enabled = True

        self.prev_speed = (self.shooter.shoot_speed, self.intake.intake_speed, self.hood.hood_speed)
    
    def execute(self):
        """Execute the control logic for the ball shooter and hood."""
        if self.enabled:
            self.shooter.shoot_speed = 1
            self.intake.intake_speed = 1
            self.hood.hood_speed = 1
        
            # Control the shooter motor based on input
            if "shooter" in self.output:
                self.shooter.enable(control=self.output["shooter"])
            else:
                self.shooter.enable(control=0)

            # Control the intake motor based on input
            if "intake" in self.output:
                self.intake.enable(control=self.output["intake"])
            else:
                self.intake.enable(control=0)

            # Control the hood motor based on input
            if "hood" in self.output:
                self.hood.enable(control=self.output["hood"])
            else:
                self.hood.enable(control=0)

    def stop(self):
        self.control(shooter=0, intake=0, hood=0)
        self.shooter.shoot_speed = self.prev_speed[0]
        self.intake.intake_speed = self.prev_speed[1]
        self.hood.hood_speed = self.prev_speed[2]
        self.enabled = False
