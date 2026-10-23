from stepper_motor import StepperMotor

class differentialDrive:
    def __init__(self, side="left", pwm_pct=15, frequency=18_000, mode="full", microsteps=4):
        self.side = side
        self.motor = StepperMotor(self.side, pwm_pct, frequency)
        self.motor.set_step_mode(mode, microsteps)

    def driveforward(self, steps, delay, direction):
        self.motor.move_stepper(steps, direction=direction, delay=delay)
        self.motor.stop()
