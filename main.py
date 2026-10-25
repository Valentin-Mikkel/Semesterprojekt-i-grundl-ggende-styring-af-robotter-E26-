import differentialDrive
from differentialDrive import DifferentialDrive
from stepper_motor import StepperMotor
import _thread
from time import sleep

side1 = "left"
side2 = "right"
pwm_pct = 0.15
frequency = 18_000
mode = "half"
microsteps = 4

left = StepperMotor(side1, pwm_pct, frequency)
left.set_step_mode(mode, microsteps)

right = StepperMotor(side2, pwm_pct, frequency)
right.set_step_mode(mode, microsteps)

motor = DifferentialDrive(left=left, right=right)

motor.move_distance(100, "forward", 0.01)
motor.turn_in_place(90, "left", 0.01)
