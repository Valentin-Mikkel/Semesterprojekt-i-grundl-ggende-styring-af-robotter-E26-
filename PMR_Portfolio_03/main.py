from stepper_motor import StepperMotor
from machine import Pin, ADC
import _thread
import time

motors = StepperMotor(pwm_pct=0.40, frequency=18_000)
motors.set_step_mode("half_step_x_axis", microsteps=4)

# Initialize ADC on GP28 (ADC2)
ldr = ADC(27)

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

end = False
def lightdata():
    global end
    start = time.ticks_ms()
    while end == False:
        # Read raw 16-bit analog value (0 to 65535)
        light_value = ldr.read_u16()

        # Calculate approximate voltage (0V to 3.3V)
        voltage = 3.3 * (light_value / 65535)

        angle = motors.getAngle()
        stop = time.ticks_diff(time.ticks_ms(), start)
        print(f"Time {stop} | Angle {angle} | Analog Value: {light_value} | Voltage: {voltage:.2f} V")
        time.sleep(0.5)

        textinput = f"Time {stop} | Angle {angle} | Analog Value: {light_value} | Voltage: {voltage:.2f} V"
        # Use with open to create a csv file for data collection
        with open('data_log.csv', 'a') as file:
            file.write(f'{textinput}\n')
            # Use flush to immediately save the data
            file.flush()


delay = 0.01
_thread.start_new_thread(lightdata, ())
turnLeft(180, delay)
time.sleep(2)
turnRight(180, delay)
end = True



'''motorleft = StepperMotor(side="left", pwm_pct=0.90, frequency=18_000)
motorright = StepperMotor(side="right", pwm_pct=0.90, frequency=18_000)

motorright.set_step_mode("micro", microsteps=4)
motorright.move_stepper(800, "forward", delay=0.001)
motorright.stop()

motorleft.set_step_mode("micro", microsteps=4)
motorleft.move_stepper(800, "forward", delay=0.001)
motorleft.stop()'''