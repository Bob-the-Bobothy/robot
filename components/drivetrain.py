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
    iters = 10
    
    def __init__(self):
        self.enabled = False

    def drive(self, input: wpimath.kinematics.ChassisSpeeds):
        """Drive robot off of ChassisSpeed

        Args:
            input (wpimath.kinematics.ChassisSpeeds): provided ChassisSpeed, delta y/dy must be ommited
        """        
        self.enabled = True
        self.desired_chassis_speed = input

    def execute(self):
        
        if self.enabled:
            # current speed
            self.wheel_speeds = self.kinematics.toWheelSpeeds(self.chassis_speed)
            self.wheel_speeds.desaturate(self.const.TOP_SPEED)
            self.states = (self.wheel_speeds.left, self.wheel_speeds.right)
            # next desired speed

            left_states = []
            right_states = []

            for i in range(self.iters):
                self.desired_wheel_speeds = self.kinematics.toWheelSpeeds(self.desired_chassis_speed)
                self.desired_wheel_speeds.desaturate(self.const.TOP_SPEED)
                left_states.append(self.desired_wheel_speeds.left)
                right_states.append(self.desired_wheel_speeds.right)

            self.desired_states = (sum(left_states) / self.iters, sum(right_states) / self.iters)

            '''self.desired_wheel_speeds = self.kinematics.toWheelSpeeds(self.desired_chassis_speed)
            self.desired_wheel_speeds.desaturate(self.const.TOP_SPEED)
            self.desired_states = (self.desired_wheel_speeds.left, self.desired_wheel_speeds.right)'''
            
            # change current speed into desired speed by feeding motors
            for desired_state, motor in zip(self.desired_states, self.drive_motors):
                motor.setVoltage(self.feed_forward.calculate(desired_state))
            
            # assuming that desired speed was reached by robot previously, (not able to check without odometry), change current speed to previously desired speed
            self.chassis_speed = self.desired_chassis_speed

        else:
            # motor safety
            self.stop()

        self.enabled = False
    
    def stop(self):
        for motor in self.drive_motors:
            motor.set(0)