import wpilib
import magicbot
from components.drivetrain import Drivetrain

class Drive:
    drive_speed = magicbot.tunable(0.7)
    drivetrain: Drivetrain

    def __init__(self):
        self.enabled = False

    def drive(self, input1=0, input2=0, mode="none"):
        self.enabled = True
        self.input1 = input1 * self.drive_speed
        self.input2 = input2 * self.drive_speed
        self.mode = mode

    def execute(self):
        if self.enabled:
            match self.mode:
                case "tank":
                    self.drivetrain.tankDrive(self.input1, self.input2)
                case "arcade":
                    self.drivetrain.arcadeDrive(self.input1, self.input2)
                case _:
                    self.drivetrain.tankDrive(0, 0)
        else:
            self.drivetrain.tankDrive(0, 0)

        self.enabled = False