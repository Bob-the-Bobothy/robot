#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import warnings

import magicbot
import wpilib
from wpilib import SmartDashboard

from components.drivetrain import Drivetrain
from components.hood import Hood
from components.intake import Intake
from components.shooter import Shooter
from controllers.drive import Drive
from util.helper_scripts import clamp


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

        self.left_motor = wpilib.VictorSP(0)
        self.right_motor = wpilib.VictorSP(1)
        self.right_motor.setInverted(True)

        self.drive_motors = (self.left_motor, self.right_motor)

        # smartdashboard stuff
        self.drive_chooser = wpilib.SendableChooser()
        self.drive_chooser.setDefaultOption("None", "none")
        self.drive_chooser.addOption("Tank Drive", "tank")
        self.drive_chooser.addOption("Arcade Drive", "arcade")

        SmartDashboard.putData(self.drive_chooser)
        
    def teleopInit(self):
        self.driver = wpilib.XboxController(0)
        self.gunner = wpilib.XboxController(1)
    
    def teleopPeriodic(self):
        with self.consumeExceptions():
            self.shooter_cont = self.gunner.getRightTriggerAxis() - self.gunner.getLeftTriggerAxis()
            self.hood_cont = round(self.gunner.getLeftY(), 2)
            self.intake_cont = int(self.gunner.getRightBumper()) - int(self.gunner.getLeftBumper())

            self.shooter.enable(self.shooter_cont)
            self.intake.enable(self.intake_cont)
            self.hood.enable(self.hood_cont)

            # safety enable
            if self.driver.getRightTriggerAxis() > 0.5:
                match self.drive_chooser.getSelected():
                    case "tank":
                        self.drive.drive(-self.driver.getLeftY(), -self.driver.getRightY(), "tank")
                    case "arcade":
                        self.drive.drive(-self.driver.getLeftY(), -self.driver.getRightX(), "arcade")
                    case _:
                        # motor safety - blank input stops motors
                        self.drive.drive()
            else:
                self.drive.drive()

            # change shooter speeds with gunner controller
            if self.gunner.getYButtonPressed():
                self.shooter.shoot_speed += 0.1
                self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
            
            if self.gunner.getAButtonPressed():
                self.shooter.shoot_speed -= 0.1
                self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
            
            self.shooter.shoot_speed += round(-self.gunner.getRightY(), 1) / 100

            self.shooter.shoot_speed = clamp(self.shooter.shoot_speed, 0, 1)
