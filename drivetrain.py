import wpilib
import wpilib.drive
import math
from wpimath.controller import SimpleMotorFeedforwardMeters

class Constants():
    def __init__(self):
        kS = 0
        kV = 2.54
        kA = 0.37
        TOP_SPEED = 4.96
        WHEELBASE = 24.375

const = Constants()

class DriveTrain(wpilib.TimedRobot):
    def __init__(self):
        self.leftMotor = wpilib.VictorSP(0)
        self.rightMotor = wpilib.VictorSP(1)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

        self.feedForward = SimpleMotorFeedforwardMeters(const.kS, const.kV, const.kA)

        self.timer = wpilib.Timer()

        self.rightMotor.setInverted(False)
        self.leftMotor.setInverted(True)
    
    def driveMotors(self, leftVelocity: float, rightVelocity: float, time):
        self.timer.restart()

        while self.timer.get() <= time:
            self.leftMotor.setVoltage(self.feedForward.calculate(leftVelocity))
            self.rightMotor.setVoltage(self.feedForward.calculate(rightVelocity))

        self.leftMotor.stopMotor
        self.rightMotor.stopMotor
    
    def driveForward(self, distance: float):
        self.driveTime = distance / const.TOP_SPEED
        self.leftSpeed, self.rightSpeed = const.TOP_SPEED
        self.timer.reset()

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)

    def turnOnSelf(self, angle):
        self.distance = 2 * math.pi * (const.WHEELBASE / 2) * (angle / 360)
        self.driveTime = self.distance / const.TOP_SPEED
        self.leftSpeed = const.TOP_SPEED
        self.rightSpeed = -1 * const.TOP_SPEED

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)