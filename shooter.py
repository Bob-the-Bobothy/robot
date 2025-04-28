import wpilib

class Shooter:
    def __init__(self):
        self.shooterMotor = wpilib.PWMSparkMax(9)
        self.intakeMotor = wpilib.PWMVictorSPX(8)

        self.shooterMotor.setSafetyEnabled(False)
        self.intakeMotor.setSafetyEnabled(False)

    def shoot(self, speed):
        # shoot at a given speed
        self.shooterMotor.set(speed)

    def intake(self, speed):
        # intake at a given speed
        self.intakeMotor.set(speed)
