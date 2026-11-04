from machine import ADC, Pin
import time


'''
Lav en class som lave opjekter inde fra main.py, ligesom med motorne, og gør det mugligt at tildele ADC pins ved oprettelse af objektet

'''

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

    '''tag data printet ovenfor at få python til at lave en .csv fil, 
    (hvis den ikke allerede eksistere) og skrive data ind i den uden den
    slette data der allerede ligge i den
    status: har prøvet at teste den, men kan ikke få serial til at virke'''
    #Use the serial port (min bruger COM4, men tjek hvad din egen computer bruger)
    #ser = serial.Serial('COM3', 9600)

    textinput = f"Analog Value: {light_value} | Voltage: {voltage:.2f} V"

    #Use with open to create a csv file for data collection
    with open('data_log.csv', 'a') as file:
        file.write(f'{textinput}\n')
        #Use flush to immediately save the data
        file.flush()
        time.sleep(1)


