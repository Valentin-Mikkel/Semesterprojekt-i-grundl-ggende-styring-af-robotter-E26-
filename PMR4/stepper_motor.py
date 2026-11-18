from machine import Pin, PWM
from time import sleep
import math


class StepperMotor:
    def __init__(self, pwm_pct=0.15, frequency=18_000):
        # Configure the four PWM outputs.
        self.pins = [
            #Left wheel pins
            PWM(Pin("GP0", Pin.OUT)),
            PWM(Pin("GP1", Pin.OUT)),
            PWM(Pin("GP2", Pin.OUT)),
            PWM(Pin("GP3", Pin.OUT)),

            # right wheel pins
            PWM(Pin("GP4", Pin.OUT)),
            PWM(Pin("GP5", Pin.OUT)),
            PWM(Pin("GP6", Pin.OUT)),
            PWM(Pin("GP7", Pin.OUT)),
            ]


        self.sequence_index = 0


        for output in self.pins:
            output.freq(frequency)

        # Store each step sequence under a separate mode name.
        # PWM duty cycle when an output is active
        val = pwm_pct
        self.val = pwm_pct

        self.full_step_sequence = [
            [val, val, 0, 0],  # Step 0
            [0, val, val, 0],  # Step 1
            [0, 0, val, val],  # Step 2
            [val, 0, 0, val],  # Step 3
        ]

        self.half_step_sequence_x_axis = [
            [val, 0, 0, 0, val, 0, 0, 0],    # Step 0
            [val, val, 0, 0, val, val, 0, 0],  # Step 1
            [0, val, 0, 0, 0, val, 0, 0],    # Step 2
            [0, val, val, 0, 0, val, val, 0],  # Step 3
            [0, 0, val, 0, 0, 0, val, 0],    # Step 4
            [0, 0, val, val, 0, 0, val, val],  # Step 5
            [0, 0, 0, val, 0, 0, 0, val],    # Step 6
            [val, 0, 0, val, val, 0, 0, val],  # Step 7
        ]

        self.half_step_sequence_y_axis = [
            [val, 0, 0, 0, 0, 0, 0, val],    # Step 0
            [val, val, 0, 0, 0, 0, val, val],  # Step 1
            [0, val, 0, 0, 0, 0, val, 0],    # Step 2
            [0, val, val, 0, 0, val, val, 0],  # Step 3
            [0, 0, val, 0, 0, val, 0, 0],    # Step 4
            [0, 0, val, val, val, val, 0, 0],  # Step 5
            [0, 0, 0, val, val, 0, 0, 0],    # Step 6
            [val, 0, 0, val, val, 0, 0, val],  # Step 7
        ]

        self.microstep_sequence = []
        # Keep track of the currently selected mode.
        self.current_sequence = self.full_step_sequence

        # some mah needed for turn and distance logic
        angle = 1.8  # angle the steppermotor turns. datablad... Fra Jes ppt
        diameter = 8  # diameter of wheels in cm

        wheelbase = 22.7  # distance between wheels in cm #MÅL BREDRE IKKE ENDELIGT MÅL

        circum = math.pi * diameter
        turningCircum = math.pi * wheelbase
        stepPR = (360 / angle) * 2 #if fullstep remove *2
        self.distPS = circum / stepPR
        self.numStepFT = turningCircum / self.distPS

        self.currentstep = 0

    def generate_microstep_sequence(self, microsteps):
        """Generate and return a complete microstep sequence."""
        if not isinstance(microsteps, int) or microsteps < 1:
            raise ValueError("microsteps must be a positive integer")

        sequence = []
        total_positions = microsteps * 4  # 4 full steps in a complete cycle
        angle_step = 2 * math.pi / total_positions


        for i in range(total_positions):
            angle = angle_step * i
            phase_a = math.cos(angle) * self.val
            phase_b = math.sin(angle) * self.val



            a_plus = max(phase_a, 0)
            a_minus = max(-phase_a, 0)
            b_plus = max(phase_b, 0)
            b_minus = max(-phase_b, 0)

            sequence.append((a_plus, b_plus, a_minus, b_minus))

        return sequence


    def set_step_mode(self, mode, microsteps=None):
        # Select full, half, or generated microstepping.
        if mode == "full":
            self.current_sequence = self.full_step_sequence
        elif mode == "half_step_x_axis":
            self.current_sequence = self.half_step_sequence_x_axis
        elif mode == "micro":
            if microsteps is None:
                raise ValueError("microsteps parameter must be provided for microstepping mode.")
            self.current_sequence = self.generate_microstep_sequence(microsteps)


    def set_step(self, step):
        """Apply one step to the selected PWM outputs."""
        for output, duty_cycle in zip(self.pins, step):
            output.duty_u16(int(duty_cycle * 65535))

    def stop(self):
        """Set the PWM duty cycle of all outputs to zero."""
        self.set_step([0, 0, 0, 0, 0, 0, 0, 0])

    def move_stepper(self, steps, direction="forward", delay=0.005):
        if direction not in ["forward", "backward", "left", "right"]:
            raise ValueError("Direction must be 'forward', 'backward', 'left', or 'right'.")
        sequence = list(self.current_sequence)
        if direction == "backward":
            sequence = list(reversed(sequence))
        if direction == "left":
            sequence = self.half_step_sequence_y_axis
        if direction == "right":
            sequence = list(reversed(self.half_step_sequence_y_axis))

        cycle = abs(steps) // len(sequence)

        try:
            for _ in range(cycle):
                for step in sequence:
                    self.set_step(step)
                    sleep(delay)
                    self.currentstep += 1
        finally:
            self.stop()


    def getAngle(self):
        angle = int(round((self.currentstep/self.numStepFT) * 360))
        return angle

    def turn(self, degree):
        steps = int(round((degree / 360) * self.numStepFT))
        return steps

    def move_distance(self, distance_cm):
        steps = distance_cm / self.distPS
        return steps