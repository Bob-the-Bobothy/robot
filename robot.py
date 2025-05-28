#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import magicbot
import wpilib
from wpilib import SmartDashboard

from components.drivetrain import Drivetrain
from components.hood import Hood
from components.intake import Intake
from components.shooter import Shooter
from controllers.drive import Drive
from controllers.ball_shooter import BallShooter
from util.helper_scripts import clamp
from util.helper_scripts import squareInput


class MyRobot(magicbot.MagicRobot):
    
    # components
    drivetrain: Drivetrain
    shooter: Shooter
    intake: Intake
    hood: Hood
    
    # controllers
    drive: Drive
    ball_shooter: BallShooter
    
    def createObjects(self):
        self.shooter_motor = wpilib.PWMSparkMax(9)
        self.intake_motor = wpilib.PWMVictorSPX(8)
        self.hood_motor = wpilib.PWMSparkMax(7)

        self.left_motor = wpilib.VictorSP(0)
        self.right_motor = wpilib.VictorSP(1)
        self.left_motor.setInverted(True)

        self.drive_motors = (self.left_motor, self.right_motor)

        # smartdashboard stuff
        self.drive_chooser = wpilib.SendableChooser()
        self.drive_chooser.setDefaultOption("None", "none")
        self.drive_chooser.addOption("Tank Drive", "tank")
        self.drive_chooser.addOption("Arcade Drive", "arcade")

        self.controller_chooser = wpilib.SendableChooser()
        self.controller_chooser.setDefaultOption("Two Controllers", 2)
        self.controller_chooser.addOption("Driver Only", 1)

        SmartDashboard.putData(self.drive_chooser)
        SmartDashboard.putData(self.controller_chooser)
        
    def teleopInit(self):
        self.intake.intake_speed = 0.7
        self.hood.hood_speed = 0.2
        self.shooter.shoot_speed = 1.0
        if wpilib.DriverStation.getJoystickIsXbox(0):
            self.driver = wpilib.XboxController(0)
        else:
            self.logger.warning("Driver controller is not connected, driving will not work")
            self.driver = False
        if wpilib.DriverStation.getJoystickIsXbox(1):
            self.gunner = wpilib.XboxController(1)
        else:
            self.logger.warning("Gunner controller not connected, shooter will not work unless one controller mode is selected")
            self.gunner = False
    
    def teleopPeriodic(self):
        with self.consumeExceptions():
            if self.gunner != False and self.controller_chooser.getSelected() == 2:
                self.shooter_cont = self.gunner.getRightTriggerAxis() - self.gunner.getLeftTriggerAxis()
                self.intake_cont = int(self.gunner.getRightBumper()) - int(self.gunner.getLeftBumper())

                self.shooter.enable(self.shooter_cont)
                self.intake.enable(self.intake_cont)

                # change shooter speeds with gunner controller
                if self.gunner.getYButtonPressed():
                    self.shooter.shoot_speed += 0.1
                    self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
                
                if self.gunner.getAButtonPressed():
                    self.shooter.shoot_speed -= 0.1
                    self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
                
                self.shooter.shoot_speed += round(-self.gunner.getRightY(), 1) / 100
                self.shooter.shoot_speed = clamp(self.shooter.shoot_speed, 0, 1)

            # safety enable
            if self.driver != False:
                if self.controller_chooser.getSelected() == 1:
                    # one controller operation
                    self.hood_cont = int(self.driver.getXButton()) - int(self.driver.getBButton())
                    self.intake_cont = int(self.driver.getRightBumper()) - int(self.driver.getLeftBumper())
                    self.shooter_cont = self.driver.getRightTriggerAxis() - self.driver.getLeftTriggerAxis()

                    self.intake.enable(self.intake_cont)
                    self.shooter.enable(self.shooter_cont)

                    if self.driver.getYButtonPressed():
                        self.shooter.shoot_speed += 0.1
                        self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
                    
                    if self.driver.getAButtonPressed():
                        self.shooter.shoot_speed -= 0.1
                        self.shooter.shoot_speed = round(self.shooter.shoot_speed, 1)
                else:
                    # two controller operation
                    self.hood_cont = self.driver.getLeftTriggerAxis() - self.driver.getRightTriggerAxis()

                    if self.driver.getLeftBumperPressed():
                        self.drive.drive_speed = 1.0
                    elif self.driver.getLeftBumperReleased():
                        self.drive.drive_speed = 0.7
                
                match self.drive_chooser.getSelected():
                    case "tank":
                        self.drive.drive("tank", self.driver.getLeftY(), self.driver.getRightY())
                    case "arcade":
                        self.drive.drive("arcade", squareInput(-self.driver.getLeftY()), squareInput(self.driver.getRightX()))
                    case _:
                        # motor safety - blank input stops motors
                        self.drive.stop()

                self.hood.enable(self.hood_cont)

            else:
                self.drive.stop()

    def disabledPeriodic(self):
        # motor safety
        self.drive.stop()
