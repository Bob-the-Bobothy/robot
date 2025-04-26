import wpilib
import wpimath
import magicbot
import wpimath
from config.constants import Constants

class Drivetrain:
    left_motor = wpilib.VictorSP(0)
    right_motor = wpilib.VictorSP(1)
    motors = (left_motor, right_motor)
    const = Constants()
    
    kinematics = wpimath.kinematics.DifferentialDriveKinematics(const.WHEELBASE)
    chassis_speed = wpimath.kinematics.ChassisSpeeds(0, 0, 0)
    feed_forward = wpimath.controller.SimpleMotorFeedforwardMeters(const.kS, const.kV, const.kA)
    
    def __init__(self):
        self.enabled = False
 
    def arcadeDrive(self, dx, omega):
        # inverse kinematics
        self.enabled = True
        self.desired_chassis_speed = wpimath.kinematics.ChassisSpeeds(dx * self.const.TOP_SPEED, 0, omega * self.const.ANGULAR_TOP_SPEED)
        
    def tankDrive(self, dleft, dright):
        # forward kinematics
        self.enabled = True
        self.desired_chassis_speed = self.kinematics.toChassisSpeed(wpimath.kinematics.DifferentialDriveWheelSpeeds(dleft * self.const.TOP_SPEED, dright * self.const.TOP_SPEED))
    
    def execute(self):
        if self.enabled:
            # current speed
            self.wheel_speeds = self.kinematics.toWheelSpeeds(self.chassis_speed)
            self.states = (self.wheel_speeds.left(), self.wheel_speeds.right())
            
            self.states = self.kinematics.desaturateWheelSpeeds(self.states, self.const.TOP_SPEED)
            
            # next desired speed
            self.desired_wheel_speeds = self.kinematics.toWheelSpeeds(self.desired_chassis_speed)
            self.desired_states = (self.wheel_speeds.left(), self.wheel_speeds.right())
            
            self.desired_states = self.kinematics.desaturateWheelSpeeds(self.desired_states, self.const.TOP_SPEED)
            
            # change current speed into desired speed
            for desired_state, state, motor in zip(self.desired_states, self.states, self.motors):
                motor.setVoltage(self.feed_forward.calculate(desired_state, state))
            
            # change current speed to previously achieved desired speed
            self.chassis_speed = self.desired_chassis_speed

        else:
            # motor safety
            self.left_motor.set(0)
            self.right_motor.set(0)