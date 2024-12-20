#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
from wpilib import SmartDashboard

import drivetrain
from drivetrain import Constants

class MyRobot(wpilib.TimedRobot):
    """
    This is a demo program showing the use of the DifferentialDrive class.
    Runs the motors with split arcade steering and an Xbox controller.
    """

    def robotInit(self):
        """Robot initialization function"""
        # Define motors
        self.driverController = wpilib.XboxController(0)
        self.drivetrain = drivetrain.DriveTrain()
        self.const = Constants()
        
        self.autoChooser = wpilib.SendableChooser()
        self.driveChooser = wpilib.SendableChooser()
        
        self.autoChooser.setDefaultOption("Stop", "stop")
        self.autoChooser.addOption("Square", "square")
        self.autoChooser.addOption("Spin", "spin")
        
        self.autoChooser.onChange(self.update)
        self.driveChooser.onChange(self.update)
        
        self.driveChooser.setDefaultOption("Stop", "stop")
        self.driveChooser.addOption("Arcade", "arcade")
        self.driveChooser.addOption("Tank", "tank")
        
        SmartDashboard.putData("Auto Mode", self.autoChooser)        
        SmartDashboard.putData("Drive Mode", self.driveChooser)
        
    def robotPeriodic(self):
        # motor safety
        self.drivetrain.robotDrive.feed()

    def disabledPeriodic(self):
        # motor safety
        self.drivetrain.robotDrive.arcadeDrive(0, 0, squareInputs=False)
        
    def update(self, input):
        self.autoSelected = input
        self.driveSelected = input

    def autonomousInit(self):
        # set up for square
        self.drivetrain.timer.restart()
        self.run = 1
        
        self.autoSelected = self.autoChooser.getSelected()
        print("Auto selected: " + self.autoSelected)

    def autonomousPeriodic(self):
        # do a square twice
        if self.autoSelected == "stop":
            self.drivetrain.robotDrive.arcadeDrive(0, 0, squareInputs=False)
        else:
            match self.autoSelected:
                case "square":
                    self.drivetrain.square(length=3, speed=2)
                case "spin":
                    self.drivetrain.robotDrive.arcadeDrive(0, 1, squareInputs=False)

    # motor safety stuff
    def teleopInit(self):
        self.drivetrain.robotDrive.arcadeDrive(0, 0, False)
        
        self.driveSelected = self.driveChooser.getSelected()
        print("Drive selected: " + self.driveSelected)

    def teleopExit(self):
        self.drivetrain.robotDrive.arcadeDrive(0, 0, False)

    def teleopPeriodic(self):
        # Drive with split arcade style
        # That means that the Y axis of the left stick moves forward
        # and backward, and the X of the right stick turns left and right.

        # controller mapping
        right_trigger = self.driverController.getRightTriggerAxis()

        # set drive mode based on triggers
        if right_trigger > 0:
            match self.driveSelected:
                case "arcade":
                    drive_mode = 0
                case "tank":
                    drive_mode = 1
                case "stop":
                    drive_mode = 2
        else:
            drive_mode = 2
            
        # stick reversing based on drive mode
        if drive_mode == 0:
            right_stick = 1 * self.driverController.getRightX()
            left_stick = -1 * self.driverController.getLeftY()
        elif drive_mode == 1:
            right_stick = -1 * self.driverController.getLeftY()
            left_stick = -1 * self.driverController.getRightY()

        ''' old code
        mapped_left_stick = 0
        mapped_right_stick = 0

        if left_stick > 0:
            mapped_left_stick = left_stick ** 2
        else:
            mapped_left_stick = -1 * (left_stick ** 2)       
        '''         

        # powers motors based on the drive mode
        if drive_mode == 0:
            self.drivetrain.robotDrive.arcadeDrive(
                left_stick, right_stick
            )
        elif drive_mode == 1:
            self.drivetrain.tankDrive(left_stick, right_stick)
        # safety condition
        elif drive_mode == 2:
            self.drivetrain.robotDrive.arcadeDrive(
                0, 0
            )

