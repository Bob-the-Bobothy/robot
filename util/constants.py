from wpimath.units import *

class Constants():
    def __init__(self):
        self.kS = 0
        self.kV: volt_seconds_per_meter = 2.38
        self.kA: volt_seconds_squared_per_meter = 0.28
        self.THEORETICAL_TOP_SPEED: meters_per_second = 5.33 #meters/seconds
        self.TOP_SPEED: meters_per_second = 5.16 #meters/seconds
        self.WHEELBASE: meters = 0.619125 #meters, diameter
        self.ANGULAR_TOP_SPEED = 16.6687 #radians/seconds
        self.WIDTH: inches = 28 #inches
        self.LENGTH: inches = 28 #inches
        self.WHEEL_DIAMETER: inches = 6 #inches
        self.WEIGHT = 45 #pounds
        self.DRIVETRAIN_RATIO = 8.46 #input/output
        self.SHOOTER_INERTIA: kilogram_square_meters = 0.0023820868 # meters^2 kilograms
        self.SHOOTER_RATIO = 2 / 3 #input to output