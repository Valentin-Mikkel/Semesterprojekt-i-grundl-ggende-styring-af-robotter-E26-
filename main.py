from differentialDrive import DifferentialDrive
from stepper_motor import StepperMotor
import _thread
from time import sleep
from machine import Pin, ADC

side1 = "left"
side2 = "right"
pwm_pct = 0.40
frequency = 18_000
mode = "half"
microsteps = 4

left = StepperMotor(side1, pwm_pct, frequency)
left.set_step_mode(mode, microsteps)

right = StepperMotor(side2, pwm_pct, frequency)
right.set_step_mode(mode, microsteps)

motor = DifferentialDrive(left=left, right=right)
'''
_thread.start_new_thread(motor.move_distance, (100, "forward", 0.02, "left"))
motor.move_distance(100, "forward", 0.02, "right")
'''
# Initialize ADC on GP28 (ADC2)
ldr = ADC(26)

# Optional: Setup onboard LED or an external relay
led = Pin("LED", Pin.OUT)

turnSide = "right"
'''
for i in range(4):
    _thread.start_new_thread(motor.move_distance, (200, "forward", 0.008, "left"))
    motor.move_distance(200, "forward", 0.008, "right")
    sleep(0.5)
    print("A")
    if turnSide == "left":
        _thread.start_new_thread(motor.turn_in_place, (90, "left", 0.008))
        motor.turn_in_place(-90, "right", 0.008)
    elif turnSide == "right":
        _thread.start_new_thread(motor.turn_in_place, (-90, "left", 0.008))
        motor.turn_in_place(90, "right", 0.008)
    sleep(0.5)
    print(i)
'''

for i in range(20): #mulig løsning af detect + kør
    light_value = ldr.read_u16()

    # Calculate approximate voltage (0V to 3.3V)
    voltage = 3.3 * (light_value / 65535)

    print(f"Analog Value: {light_value} | Voltage: {voltage:.2f} V")

    # Example logic: Turn on LED if it gets dark
    if light_value > 40000:
        led.value(1)  # Turn LED ON in darkness
        #_thread.start_new_thread(motor.move_distance, (50, "forward", 0.1, "left"))
        motor.move_distance(3, "forward", 0.1, "right")
    else:
        led.value(0)  # Turn LED OFF in light
        #_thread.start_new_thread(motor.turn_in_place, (90, "left", 0.1))
        motor.turn_in_place(3, "left", 0.1)

    sleep(0.2)