from stepper_motor import StepperMotor
import _thread

motorleft = StepperMotor(side="left", pwm_pct=0.35, frequency=18_000)
motorright = StepperMotor(side="right", pwm_pct=0.35, frequency=18_000)

motorright.set_step_mode("micro", microsteps=4)
motorleft.set_step_mode("micro", microsteps=4)

def driveforwardleft(steps, delay):
    motorleft.move_stepper(steps, "forward", delay)
    motorleft.stop()

def driveforwardright(steps, delay):
    motorright.move_stepper(steps, "forward", delay)
    motorright.stop()

while True:

    _thread.start_new_thread(driveforwardleft,(800,0.001))
    driveforwardright(800, 0.001)


'''motorleft = StepperMotor(side="left", pwm_pct=0.90, frequency=18_000)
motorright = StepperMotor(side="right", pwm_pct=0.90, frequency=18_000)

motorright.set_step_mode("micro", microsteps=4)
motorright.move_stepper(800, "forward", delay=0.001)
motorright.stop()

motorleft.set_step_mode("micro", microsteps=4)
motorleft.move_stepper(800, "forward", delay=0.001)
motorleft.stop()'''