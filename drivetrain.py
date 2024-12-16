import wpilib
import wpilib.drive
import math
from wpimath.controller import SimpleMotorFeedforwardMeters

# important constants calculated previously
class Constants():
    def __init__(self):
        self.kS = 0
        self.kV = 2.38
        self.kA = 0.28
        self.THEORETICAL_TOP_SPEED = 5.33 #m/s
        self.TOP_SPEED = 5.16 #m/s
        self.WHEELBASE = 0.619125 #meters

const = Constants()

# whole system for auto and teleop
class DriveTrain():
    def __init__(self):
        # define variables for drivetrain
        self.leftMotor = wpilib.VictorSP(0)
        self.rightMotor = wpilib.VictorSP(1)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

        self.feedForward = SimpleMotorFeedforwardMeters(const.kS, const.kV, const.kA)

        self.timer = wpilib.Timer()

        self.rightMotor.setInverted(False)
        self.leftMotor.setInverted(True)
        
        self.robotDrive.setSafetyEnabled(False)
        self.robotDrive.setMaxOutput(0.7)
    
    def driveMotors(self, leftVelocity: float, rightVelocity: float, time):
        # drive motors for a given time and speed

        self.timer.restart()

        while self.timer.get() <= time:
            self.leftMotor.setVoltage(self.feedForward.calculate(leftVelocity))
            self.rightMotor.setVoltage(self.feedForward.calculate(rightVelocity))

        # motor safety
        self.leftMotor.stopMotor
        self.rightMotor.stopMotor

    def tankDrive(self, leftStick: float, rightStick: float):
        # drive off left and right sticks
        self.leftMotor.setVoltage(self.feedForward.calculate(leftStick * const.TOP_SPEED))
        self.rightMotor.setVoltage(self.feedForward.calculate(rightStick * const.TOP_SPEED))
    
    def driveForward(self, distance: float, speed=const.TOP_SPEED):
        # drive off distance and speed

        self.driveTime = distance / speed
        self.leftSpeed = speed
        self.rightSpeed = speed
        self.timer.reset()

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)

    def turnOnSelf(self, angle, speed=const.TOP_SPEED):
        # drive off angle and speed

        self.distance = 4 * math.pi * const.WHEELBASE * (angle / 360)
        self.driveTime = self.distance / speed

        # make it turn instead of go straight
        self.leftSpeed = speed
        self.rightSpeed = -1 * speed

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)
    
    # pause for an amount of time
    def stopDriving(self, time: float):
        self.driveMotors(0, 0, time)

    def square(self, length, speed):
        for i in range(4):
            self.driveForward(length, speed)
            self.stopDriving(0.3)
            self.turnOnSelf(90, 2)
            self.stopDriving(0.3)

    def circle(self, angle, speed):
        self.distance = math.pi * const.WHEELBASE * (angle / 360)
        self.driveTime = self.distance / speed

        self.leftSpeed = 0
        self.rightSpeed = speed
        
        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)