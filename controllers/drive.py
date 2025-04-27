import wpilib
import magicbot
from components.drivetrain import Drivetrain

from wpimath.kinematics import ChassisSpeeds, DifferentialDriveWheelSpeeds as WheelSpeeds
from util.constants import Constants

class Drive:
    drive_speed = magicbot.tunable(0.7)
    drivetrain: Drivetrain
    const = Constants()

    def __init__(self):
        self.enabled = False

    def drive(self, mode="arcade", /, *args):
        """Converts multiple different inputs to ChassisSpeeds for driving

        Args:
            mode (str, optional): Teleop Drive Mode, necessary for stick driving. Defaults to "arcade".

        Raises:
            TypeError: If a non valid type positional arg is supplied or > 3 args supplied a TypeError will raise
        """


        # process args into proper form
        for arg in args:
            if isinstance(arg, ChassisSpeeds): #chassis speed drive
                self.enabled = True
                vx = arg.vx
                omega = arg.omega
                self.output = ChassisSpeeds(vx * self.drive_speed, 0, omega * self.drive_speed)
                break
            elif isinstance(arg, float): #stick drive - implemented as arcade
                self.enabled = True
                if "input1" not in locals():
                    input1 = arg
                elif "input2" not in locals():
                    input2 = arg
                if "input1" in locals() and "input2" in locals():
                    if mode == "arcade":
                        self.output = ChassisSpeeds(input1 * self.const.TOP_SPEED * self.drive_speed, 0, input2 * self.const.ANGULAR_TOP_SPEED * self.drive_speed)
                    if mode == "tank":
                        wheels = WheelSpeeds(input1 * self.const.TOP_SPEED * self.drive_speed, input2 * self.const.TOP_SPEED * self.drive_speed)
                        self.output = self.drivetrain.kinematics.toChassisSpeeds(wheels)
                    break
            elif isinstance(arg, WheelSpeeds):
                self.enabled = True
                arg.desaturate(self.const.TOP_SPEED * self.drive_speed)
                self.output = self.drivetrain.kinematics.toChassisSpeeds(arg)
                break
            else:
                self.enabled = False
                

    def execute(self):
        if self.enabled:
            self.drivetrain.drive(self.output)

        else:
            self.stop()

        self.enabled = False

    def stop(self):
        self.drivetrain.stop()