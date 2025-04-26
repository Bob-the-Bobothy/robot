from magicbot import StateMachine, state, timed_state

from components.shooter import Shooter
from components.hood import Hood
from components.intake import Intake

class BallShooter(StateMachine):
    shooter: Shooter
    intake: Intake
    hood: Hood
    
    def fire(self):
        self.engage()
        
    @timed_state(first=True, duration=1.5, next_state="firing")
    def prepare_to_fire(self):
        self.shooter.enable(control=1)
    
    @timed_state(duration=1, must_finish=True)
    def firing(self):
        self.shooter.enable(control=1)
        self.intake.feed(control=1)
