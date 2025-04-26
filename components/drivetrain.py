import magicbot
import wpilib
import wpimath
import wpimath.controller

from util.constants import Constants

from wpimath.units import *


class Drivetrain:
    drive_motors: tuple

    const = Constants()
    
    kinematics = wpimath.kinematics.DifferentialDriveKinematics(const.WHEELBASE)
    chassis_speed = wpimath.kinematics.ChassisSpeeds(0, 0, 0)
    feed_forward = wpimath.controller.SimpleMotorFeedforwardMeters(const.kS, const.kV, const.kA)
    states = (0, 0)
    
    def __init__(self):
        self.enabled = False

    def autoDrive(self, left: meters_per_second=const.TOP_SPEED, right: meters_per_second=const.TOP_SPEED): # type: ignore
        # true pure driving
        self.enabled = True
        self.local_drive = False
        self.desired_states = (left, right)
 
    def arcadeDrive(self, dx, omega):
        # inverse kinematics - convert chassis speed to wheelspeeds
        self.local_drive = True
        self.enabled = True
        self.desired_chassis_speed = wpimath.kinematics.ChassisSpeeds(dx * self.const.TOP_SPEED, 0, omega * self.const.ANGULAR_TOP_SPEED)
        
    def tankDrive(self, dleft, dright):
        # forward kinematics - convert wheelspeeds to chassis speed
        self.local_drive = True
        self.enabled = True
        self.desired_chassis_speed = self.kinematics.toChassisSpeeds(wpimath.kinematics.DifferentialDriveWheelSpeeds(dleft * self.const.TOP_SPEED, dright * self.const.TOP_SPEED))
    
    def execute(self):
        if self.enabled:
            # local drive is teleop
            if self.local_drive:
                # current speed
                self.wheel_speeds = self.kinematics.toWheelSpeeds(self.chassis_speed)
                self.wheel_speeds.desaturate(self.const.TOP_SPEED)
                self.states = (self.wheel_speeds.left, self.wheel_speeds.right)

                # next desired speed
                self.desired_wheel_speeds = self.kinematics.toWheelSpeeds(self.desired_chassis_speed)
                self.desired_wheel_speeds.desaturate(self.const.TOP_SPEED)

                self.desired_states = (self.desired_wheel_speeds.left, self.desired_wheel_speeds.right)
                
                # change current speed into desired speed
                for desired_state, state, motor in zip(self.desired_states, self.states, self.drive_motors):
                    motor.setVoltage(self.feed_forward.calculate(desired_state, state))
                
                # change current speed to previously achieved desired speed
                self.chassis_speed = self.desired_chassis_speed
            # not local drive is auto
            else:
                # drive purely off of wheelspeed for auto
                for desired_state, state, motor in zip(self.desired_states, self.states, self.drive_motors):
                    motor.setVoltage(self.feed_forward.calculate(desired_state, state))

                self.states = self.desired_states

        else:
            # motor safety
            for motor in self.drive_motors:
                motor.set(0)

        self.enabled = False