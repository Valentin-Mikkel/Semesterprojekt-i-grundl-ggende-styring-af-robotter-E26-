from stepper_motor import StepperMotor
from machine import Pin, ADC
import _thread
import time

# Initialize ADC on GP28 (ADC2)
ldr = ADC(27)
ldr2 = ADC(26)
direction = "undecided"
value = 0
#delay = round(-0.0000005*value+0.025, 4) equation for right and backwards movement
#delay = round(0.0000004*value-0.0058, 4) equation for forward and left movement

motors = StepperMotor(pwm_pct=0.40, frequency=18_000)
motors.set_step_mode("half_step_x_axis", microsteps=4)

def driveforward(steps, delay):
    motors.move_stepper(steps, "forward", delay=delay)

def driveleft(steps, delay):
    motors.move_stepper(steps, "left", delay=delay)

def driveright(steps, delay):
    motors.move_stepper(steps, "right", delay=delay)

def drivebackward(steps, delay):
    motors.move_stepper(steps, "backward", delay=delay)

def turnLeft(degree, delay):
    steps = motors.turn(degree)
    motors.move_stepper(steps, "left", delay=delay)

def turnRight(degree, delay):
    steps = motors.turn(degree)
    motors.move_stepper(steps, "right", delay=delay)

def distanceforward(distance, delay):
    steps = motors.move_distance(distance)
    motors.move_stepper(motors.move_stepper(steps, "forward", delay=delay))

def distancebackward(distance, delay):
    steps = motors.move_distance(distance)
    motors.move_stepper(motors.move_stepper(steps, "backward", delay=delay))

step = 100
degree = 25
while True:
    y = ldr.read_u16()
    x = ldr2.read_u16()

    if x >= 60000:
        print("emergency stop")
        motors.stop()
        break

    if y >= 28000:
        direction = "right"
        delay = 0.001
        driveright(degree, delay)
    elif y <= 18000:
        direction = "left"
        delay = 0.001
        driveleft(degree, delay)
    elif x >= 28000:
        direction = "backwards"
        delay = 0.001
        drivebackward(step, delay)
    elif x <= 18000:
        direction = "forward"
        delay = 0.001
        driveforward(step, delay)

    output = f"x = {x} | y = {y} | direction {direction}"
    print(output)



