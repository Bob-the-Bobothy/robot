import wpilib
#from wpimath.system import *
from wpimath.system.plant import *
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics.units import units
from wpilib import Field2d, SmartDashboard
from wpilib.simulation import *

from util.constants import Constants


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface):
        self.physics_controller = physics_controller
        self.const = Constants()

        self.l_motor = wpilib.simulation.PWMSim(0)
        self.r_motor = wpilib.simulation.PWMSim(1)

        '''self.shooter_motor = wpilib.simulation.PWMSim(9)
        self.intake_motor = wpilib.simulation.PWMSim(8)

        self.shooter_system = LinearSystemId.flywheelSystem(DCMotor.CIM(1), self.const.SHOOTER_INERTIA, self.const.SHOOTER_RATIO)
        self.shooter_sim = FlywheelSim(self.shooter_system, DCMotor.CIM(1), self.const.SHOOTER_RATIO)'''

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,                   # motor configuration
            self.const.WEIGHT * units.lbs,              # robot mass
            self.const.DRIVETRAIN_RATIO,                # drivetrain gear ratio
            2,                                          # motors per side
            self.const.WHEELBASE * units.meters,        # robot wheelbase
            self.const.WIDTH * units.inch * 2,          # robot width
            self.const.LENGTH * units.inch * 2,         # robot length
            self.const.WHEEL_DIAMETER * units.inch      # wheel diameter
        )

        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)
        

    def update_sim(self, now: float, tm_diff: float) -> None:
        l_motor = self.l_motor.getSpeed()
        r_motor = self.r_motor.getSpeed()

        transform = self.drivetrain.calculate(l_motor, r_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)

        self.field.setRobotPose(pose)
        SmartDashboard.putData("Field", self.field)
