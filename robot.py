#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import magicbot
from components.drivetrain import Drivetrain
from components.intake import Intake
from components.hood import Hood
from components.shooter import Shooter
from controllers.drive import Drive

class MyRobot(magicbot.MagicRobot):
    
    # components
    drivetrain: Drivetrain
    shooter: Shooter
    intake: Intake
    hood: Hood
    
    # controllers
    drive: Drive
    
    def createObjects(self):
        self.shooter_motor = wpilib.PWMSparkMax(9)
        self.intake_motor = wpilib.PWMVictorSPX(8)
        self.hood_motor = wpilib.PWMSparkMax(7)
        self.clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        
    def teleopInit(self):
        self.driver = wpilib.XboxController(0)
        self.gunner = wpilib.XboxController(1)
        self.mode = magicbot.tunable("none")
        self.drive_speed = self.clamp(magicbot.tunable(0.7), 0, 1)
    
    def teleopPeriodic(self):
        match self.mode:
            case "tank":
                self.drivetrain.arcadeDrive(self.driver.getLeftY() * self.drive_speed, self.driver.getRightY() * self.drive_speed)
            case "arcade":
                self.drivetrain.arcadeDrive(self.driver.getLeftY() * self.drive_speed, self.driver.getRightX() * self.drive_speed)
