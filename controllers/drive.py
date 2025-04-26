import wpilib
import magicbot

from components.drivetrain import Drivetrain

class Drive:
    drivetrain: Drivetrain
    
    mode = magicbot.tunable("none")

    def drive(self, control0, control1):
        match self.mode:
            case "arcade":
                self.drivetrain.arcadeDrive(control0, control1)
            case "tank":
                self.drivetrain.tankDrive(control0, control1)