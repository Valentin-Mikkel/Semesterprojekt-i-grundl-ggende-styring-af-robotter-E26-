from machine import ADC, Pin
import time


'''
Lav en class som lave opjekter inde fra main.py, ligesom med motorne, og gør det mugligt at tildele ADC pins ved oprettelse af objektet

'''
class ADCPin:
    def __init__(self, pins):
        self._pins = pins #Tilføj mulighed for at indsætte/vælge pins i main
        self._adc = [
            ADC(26), #left
            ADC(27), #mid
            ADC(28), #right
        ]


    def read_value(self):
        #indsæt så den læser værdier fra de specifikke pins
        left_ldr = self._adc[0]
        mid_ldr = self._adc[1]
        right_ldr = self._adc[2]

        #Læser light value fra hver enkelt adc pin/ ldr sensor
        light_value_left = left_ldr.read_u16()
        light_value_mid = mid_ldr.read_u16()
        light_value_right = right_ldr.read_u16()

        #Calculate the voltage for each ldr
        voltage_left = 3.3 * (light_value_left / 65535)
        voltage_mid = 3.3 * (light_value_mid / 65535)
        voltage_right = 3.3 * (light_value_right / 65535)

        #??print værdier fra hver ldr??
        print(f"Analog Value for left ldr: {light_value_left} | Voltage for left ldr: {voltage_left:.2f} V\n"
              f"Analog Value for mid ldr: {light_value_mid} | Voltage for mid ldr: {voltage_mid:.2f} V\n"
              f"Analog Value for right ldr: {light_value_right} | Voltage for right ldr: {voltage_right:.2f} V\n"
              f"__________________________________________________________"
        )
    #def bool status sides ldr
    #def status enum mid ldr

'''
# Initialize ADC on GP28 (ADC2)
#ldr = ADC(26)

# Optional: Setup onboard LED or an external relay
led = Pin("LED", Pin.OUT) # DEBUGGING

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

    tag data printet ovenfor at få python til at lave en .csv fil, 
    (hvis den ikke allerede eksistere) og skrive data ind i den uden den
    slette data der allerede ligge i den
    status: har prøvet at teste den, men kan ikke få serial til at virke
    #Use the serial port (min bruger COM4, men tjek hvad din egen computer bruger)
    #ser = serial.Serial('COM3', 9600)

    textinput = f"Analog Value: {light_value} | Voltage: {voltage:.2f} V"

    #Use with open to create a csv file for data collection
    with open('data_log.csv', 'a') as file:
        file.write(f'{textinput}\n')
        #Use flush to immediately save the data
        file.flush()
        time.sleep(1)


'''