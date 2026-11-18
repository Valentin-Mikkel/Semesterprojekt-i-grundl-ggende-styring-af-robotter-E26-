import network
import time
import socket
from machine import Pin, ADC
import _thread

ap = network.WLAN(network.AP_IF)
ap.config(essid="RobtekGroup6", password="RobtekGroup1234")
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
        print("Received data:", data.decode(), "from", addr)
    except OSError:
        pass

    time.sleep(0.1)
