from machine import ADC, Pin
import time

# Initialize ADC on GP28 (ADC2)
ldr = ADC(26)

# Optional: Setup onboard LED or an external relay
led = Pin("LED", Pin.OUT)

while True:
    # Read raw 16-bit analog value (0 to 65535)
    light_value = ldr.read_u16()

    # Calculate approximate voltage (0V to 3.3V)
    voltage = 3.3 * (light_value / 65535)

    print(f"Analog Value: {light_value} | Voltage: {voltage:.2f} V")

    # Example logic: Turn on LED if it gets dark
    if light_value > 40000:
        led.value(1)  # Turn LED ON in darkness
    else:
        led.value(0)  # Turn LED OFF in light

    time.sleep(1)