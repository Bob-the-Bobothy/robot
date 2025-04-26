from magicbot import StateMachine, state, timed_state

from components.shooter import Shooter
from components.hood import Hood
from components.intake import Intake

class BallShooter(StateMachine):
    shooter: Shooter
    intake: Intake
    hood: Hood