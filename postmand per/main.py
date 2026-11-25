from stepper_motor import StepperMotor
from machine import ADC
import time

motors = StepperMotor(pwm_pct=0.40, frequency=18_000)
motors.set_step_mode("half_step_x_axis", microsteps=4)

leftlight = "white"
rightlight = "white"
forwardlight = "white"
step = 8
delay = 0.001

def findintecept():
    global leftlight, rightlight, step
    while leftlight == "white" and rightlight == "white":
        motors.move_stepper(step, "forward", delay=delay)
        leftlight = "black"

def forward():
    steps = int(round(motors.move_distance(6)))
    motors.move_stepper(steps, "forward", delay=delay)

def right():
    global forwardlight, rightlight, step
    steps = motors.turn(30)
    motors.move_stepper(steps, "right", delay=delay)
    while forwardlight != "black":
        motors.move_stepper(step, "right", delay=delay)
        forwardlight = "black"

def left():
    global forwardlight, leftlight, step
    steps = motors.turn(30)
    motors.move_stepper(steps, "left", delay=delay)
    while forwardlight != "black":
        motors.move_stepper(step, "left", delay=delay)
        forwardlight = "black"

def turnaround():
    global forwardlight, rightlight, step
    steps = motors.turn(120)
    motors.move_stepper(steps, "right", delay=delay)
    while forwardlight != "black":
        motors.move_stepper(steps, "right", delay=delay)
        forwardlight = "black"

#main
sequence = [
    "forward", "right", "forward", "forward", "turn around", 
    "forward", "right", "turn around",
    "left", "forward", "turn around", 
    "right", "forward", "forward", "right", "turn around",
    "left", "forward", "forward", "left", "turn around",
    "forward", "forward", "right", "left", "forward", "turn around",
    "forward", "right", "left", "forward", "forward", "turn around",
    "forward", "forward", "right", "left", "right", "right", "turn around",
    "right", "right", "left", "left", "turn around",
    "left", "left", "left", "turn around",
    "right", "right", "right", "turn around",
    "right", "right", "right", "turn around",
    "left", "left", "left", "turn around",
    "left", "left", "right", "right", "turn around",
    "left", "left", "right", "right", "turn around",
    "right", "forward", "right", "left", "right", "left", "turn around",
    "left", "left", "turn around",
    "right", "forward", "forward", "forward", "right", "turn around",
    "forward", "right", "forward", "right", "turn around",
    "right", "right", "left", "forward", "forward", "turn around"]

currentnode = "ST"
for i in range(len(sequence)):
    leftlight = "white"
    rightlight = "white"
    forwardlight = "white"
    if sequence[i] == "forward":
        a = "forward"
        forward()
    elif sequence[i] == "right":
        a = "right"
        right()
    elif sequence[i] == "left":
        a = "left"
        left()
    elif sequence[i] == "turn around":
        a = "[ turn around ]"
        turnaround()

    print(sequence[i] + a)
    findintecept()