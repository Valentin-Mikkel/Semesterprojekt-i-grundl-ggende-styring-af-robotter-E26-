from stepper_motor import StepperMotor
from machine import ADC, Pin
import network
import time
import socket
import _thread


direction = "undecided"
emergency_stop_active = False
command = "no command"
current_speed = 1
delay = 0.008


emg_btn = Pin(8, Pin.IN, Pin.PULL_UP)

motors = StepperMotor(pwm_pct=0.40, frequency=18_000)
motors.set_step_mode("half_step_x_axis", microsteps=4)

def driveforward(steps, delay):
    motors.move_stepper(steps, "forward", delay=delay)

def drivebackward(steps, delay):
    motors.move_stepper(steps, "backward", delay=delay)

def turnLeft(degree, delay):
    motors.move_stepper(step, "left", delay=delay)

def turnRight(degree, delay):
    motors.move_stepper(step, "right", delay=delay)

def distanceforward(distance, delay):
    steps = motors.move_distance(distance)
    motors.move_stepper(steps, "forward", delay=delay)

def distancebackward(distance, delay):
    steps = motors.move_distance(distance)
    motors.move_stepper(steps, "backward", delay=delay)

def driveright(steps, delay):
    motors.move_stepper(steps, "forwardright", delay=delay)

def driveleft(steps, delay):
    motors.move_stepper(steps, "forwardleft", delay=delay)


step = 8
degree = 25

'''
while True:
    y = ysen.read_u16()
    x = xsen.read_u16()

    if x >= 60000:
        print("emergency stop")
        motors.stop()
        stop = True
        while x >= 60000:
            x = xsen.read_u16()
            print(x)
        while stop:
            x = xsen.read_u16()
            print(x)
            if x >= 60000:
                while x >= 60000:
                    x = xsen.read_u16()
                stop = False

    if y >= 28000:
        direction = "right"
        delay = 0.001
        driveleft(degree, delay)
    elif y <= 18000:
        direction = "left"
        delay = 0.001
        driveright(degree, delay)
    elif 28000 <= x <= 60000:
        direction = "backwards"
        delay = 0.001
        drivebackward(step, delay)
    elif x <= 18000:
        direction = "forward"
        delay = 0.001
        driveforward(step, delay)

    output = f"x = {x} | y = {y} | direction {direction}"
    print(output)
    '''

ap = network.WLAN(network.AP_IF)
ap.config(ssid="RobtekGroup6", password="RobtekGroup1234")
ap.active(True)

while not ap.active():
    pass

print("Wireless transmitter is active. Network config:", ap.ifconfig()[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 1000))
sock.setblocking(False)

print("Wireless transmitter is listening...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip()
    except OSError:
        pass

    if emg_btn.value() == 0:
        if not emergency_stop_active:
            print("Emergency stop")
        motors.stop()
        break


    if command == "change speed":
        if current_speed == 1:
            current_speed = 2
            delay = 0.004
        elif current_speed == 2:
            current_speed = 3
            delay = 0.001
        elif current_speed == 3:
            current_speed = 1
            delay = 0.008

    elif command == "Drive Forward":
        print("Command 'Drive Forward' received. Executing action...")
        direction = "forward"
        driveforward(step, delay)


    elif command == "Drive Backward":
        print("Command 'Drive Backward' received. Executing action...")
        direction = "backwards"
        drivebackward(step, delay)

    elif command == "Turn Left":
        print("Command 'Turn Left' received. Executing action...")
        direction = "left"
        turnLeft(degree, delay)

    elif command == "Turn Right":
        print("Command 'Turn Right' received. Executing action...")
        direction = "right"
        turnRight(degree, delay)

    elif command == "drive left":
        print("Command 'drive left' received. Executing action...")
        direction = "left"
        driveleft(step, delay)

    elif command == "drive right":
        print("Command 'drive right' received. Executing action...")
        direction = "right"
        driveright(step, delay)

    elif command == "no command":
        motors.stop()





