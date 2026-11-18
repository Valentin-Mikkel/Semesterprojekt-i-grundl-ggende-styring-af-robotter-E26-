from itertools import count

import network
import time
import socket
from machine import Pin, ADC
import _thread


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("RobtekGroup6", "RobtekGroup1234")

print("connecting to wireless transmitter...")
while not wlan.isconnected():
    pass

print("Wireless receiver is connected to transmitter. Network config:", wlan.ifconfig()[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Robot_IP = "192.168.4.1"
Robot_PORT = 1000

counter = 0
while True:
    counter += 1
    message = f"Hello from receiver! Count: {counter}"
    sock.sendto(message.encode(), (Robot_IP, Robot_PORT))
    print("Sent data:", message)
    time.sleep(1)