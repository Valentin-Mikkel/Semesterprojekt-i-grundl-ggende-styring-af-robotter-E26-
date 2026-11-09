from stepper_motor import StepperMotor
import _thread


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


turnLeft(3600, 0.001)
while True:
    '''
    driveforward(800, 0.001)
    driveleft(800, 0.001)
    driveforward(800, 0.001)
    driveright(800, 0.001)
    drivebackward(800, 0.001)
    '''




'''motorleft = StepperMotor(side="left", pwm_pct=0.90, frequency=18_000)
motorright = StepperMotor(side="right", pwm_pct=0.90, frequency=18_000)

motorright.set_step_mode("micro", microsteps=4)
motorright.move_stepper(800, "forward", delay=0.001)
motorright.stop()

motorleft.set_step_mode("micro", microsteps=4)
motorleft.move_stepper(800, "forward", delay=0.001)
motorleft.stop()'''