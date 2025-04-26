import typing

import wpilib
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics.units import units
from wpilib import Field2d, SmartDashboard

from robot import MyRobot
from util.constants import Constants

if typing.TYPE_CHECKING:
    from robot import MyRobot

class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface):
        self.physics_controller = physics_controller
        self.const = Constants()

        self.l_motor = wpilib.simulation.PWMSim(0)
        self.r_motor = wpilib.simulation.PWMSim(1)

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            50 * units.lbs,                    # robot mass
            8.64,                              # drivetrain gear ratio
            2,                                  # motors per side
            self.const.WHEELBASE * units.meters,                    # robot wheelbase
            28 * units.inch * 2, # robot width
            28 * units.inch * 2, # robot length
            6 * units.inch,                     # wheel diameter
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
