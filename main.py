from differentialDrive import differentialDrive
import _thread
from time import sleep

left = differentialDrive(side="left", pwm_pct=0.35, frequency=18_000, mode="micro", microsteps=4)
right = differentialDrive(side="right", pwm_pct=0.35, frequency=18_000, mode="micro", microsteps=4)

while True:
    _thread.start_new_thread(left.driveforward,(800, 0.001,"forward"))
    right.driveforward(800, 0.001,"forward")
    sleep(1)
'''
delay = 0.01
for i in range(4):
    turning = round(motor.turn(90))
    motor.move_steps(turning, delay, direction="forward")

    sleep(1)
    #motor.move_steps(-turning, delay=0.01, direction="forward")
    path = round(motor.travelStep(100))
    print(path)
    motor.move_steps(path, delay, direction="forward")
    sleep (1)
'''


'''motorleft = StepperMotor(side="left", pwm_pct=0.90, frequency=18_000)
motorright = StepperMotor(side="right", pwm_pct=0.90, frequency=18_000)

motorright.set_step_mode("micro", microsteps=4)
motorright.move_stepper(800, "forward", delay=0.001)
motorright.stop()

motorleft.set_step_mode("micro", microsteps=4)
motorleft.move_stepper(800, "forward", delay=0.001)
motorleft.stop()'''