#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import math
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
        
    def robotPeriodic(self):
        self.drivetrain.robotDrive.feed()

    def autonomousInit(self):
        self.drivetrain.timer.restart()
        self.run = 1

    def autonomousPeriodic(self):
        # do a square
        if self.run > 0:
            for i in range(4):
                self.drivetrain.driveForward(5, 2)
                self.drivetrain.turnOnSelf(90, self.const.TOP_SPEED)

            self.run = 0
        
        self.drivetrain.robotDrive.arcadeDrive(0, 0)

    def teleopInit(self):
        self.drivetrain.robotDrive.arcadeDrive(0, 0, False)

    def teleopExit(self):
        self.drivetrain.robotDrive.arcadeDrive(0, 0, False)

    def teleopPeriodic(self):
        # Drive with split arcade style
        # That means that the Y axis of the left stick moves forward
        # and backward, and the X of the right stick turns left and right.

        # establish a variable to differentiate between tank and arcade drive
        drive_mode = 0

        # controller mapping
        right_trigger = self.driverController.getRightTriggerAxis()
        left_trigger = self.driverController.getLeftTriggerAxis()
        left_bumper = 0

        if self.driverController.getLeftBumper() > 0:
            if left_bumper == 0:
                left_bumper = 1
            elif left_bumper == 1:
                left_bumper = 0
        
        if left_bumper == 0:
            self.drivetrain.robotDrive.setMaxOutput(0.7)
        elif left_bumper == 1:
            self.drivetrain.robotDrive.setMaxOutput(1.0)

        # set drive mode based on triggers
        if right_trigger > 0 and left_trigger <= 0:
            drive_mode = 0
        elif left_trigger > 0 and right_trigger <= 0:
            drive_mode = 1
        else: # if both buttons are pressed it turns off
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
            self.drivetrain.robotDrive.tankDrive(
                left_stick, right_stick
            )
        # safety condition
        elif drive_mode == 2:
            self.drivetrain.robotDrive.arcadeDrive(
                0, 0
            )

