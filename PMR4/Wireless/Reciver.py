import network
import time
import socket
from machine import Pin, ADC
import _thread


joyx = ADC(26)
joyy = ADC(27)
btnjoy = Pin(18, Pin.IN, Pin.PULL_UP)
prev_btn = 1

current_speed = 1
speed_led_33p = Pin(19, Pin.OUT)
speed_led_66p = Pin(20, Pin.OUT)
speed_led_100p = Pin(21, Pin.OUT)

speed_led_33p.value(1)
speed_led_66p.value(0)
speed_led_100p.value(0)



wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("RobtekGroup6", "RobtekGroup1234")
wlan.config(pm=0xa11140)

print("connecting to wireless transmitter...")
while not wlan.isconnected():
    time.sleep(0.5)

print("Wireless receiver is connected to transmitter. Network config:", wlan.ifconfig()[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Robot_IP = "192.168.4.1"
Robot_PORT = 1000

counter = 0
while True:


    joyx_value = joyx.read_u16()
    joyy_value = joyy.read_u16()
    btnjoy_value = btnjoy.value()

    print(f"JoyX: {joyx_value}, JoyY: {joyy_value}, Button: {btnjoy_value}")

    if btnjoy_value == 0 and prev_btn == 1:  # Button pressed, not held
        if current_speed == 1:
            current_speed = 2
            speed_led_33p.value(1)
            speed_led_66p.value(1)
            speed_led_100p.value(0)
        elif current_speed == 2:
            current_speed = 3
            speed_led_33p.value(1)
            speed_led_66p.value(1)
            speed_led_100p.value(1)
        elif current_speed == 3:
            current_speed = 1
            speed_led_33p.value(1)
            speed_led_66p.value(0)
            speed_led_100p.value(0)

        sock.sendto("change speed".encode(), (Robot_IP, Robot_PORT))

    if joyy_value > 60000 and joyx_value >= 45000:
        message = "drive right"
    elif joyy_value > 60000 and joyx_value <= 20000:
        message = "drive left"
    elif joyy_value > 60000:
        message = "Drive Forward"
    elif joyy_value <= 1000:
        message = "Drive Backward"
    elif joyx_value >= 60000:
        message = "Turn Left"
    elif joyx_value <= 1000:
        message = "Turn Right"

    else:
        message = "no command"



    sock.sendto(message.encode(), (Robot_IP, Robot_PORT))
    print("Sent data:", message)

    prev_btn = btnjoy_value
    time.sleep(0.1)


