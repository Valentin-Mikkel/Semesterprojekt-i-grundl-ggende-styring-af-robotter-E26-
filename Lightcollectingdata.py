from machine import ADC, Pin
import time
import serial

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

    '''tag data printet ovenfor at få python til at lave en .csv fil, 
    (hvis den ikke allerede eksistere) og skrive data ind i den uden den
    slette data der allerede ligge i den
    status: har prøvet at teste den, men kan ikke få serial til at virke'''
    #Use the serial port (min bruger COM4, men tjek hvad din egen computer bruger)
    ser = serial.Serial('COM4', 9600)

    #Use with open to create a csv file for data collection
    with open('data_log.csv', 'a') as file:
        while True: #Read the line from the terminal, and print it
            line = ser.readline().decode('utf-8').strip()
            print(line)
        #Append the data to the data file
            file.write(f'{line}\n')
            #Use flush to immediately save the data
            file.flush()
            time.sleep(1)


    # Example logic: Turn on LED if it gets dark
    if light_value > 40000:
        led.value(1)  # Turn LED ON in darkness
    else:
        led.value(0)  # Turn LED OFF in light

    time.sleep(1)