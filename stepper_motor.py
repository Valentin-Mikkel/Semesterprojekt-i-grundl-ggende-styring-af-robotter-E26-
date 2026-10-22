from machine import Pin, PWM
from time import sleep
import math


class StepperMotor:
    def __init__(self, side, pwm_pct=0.15, frequency=18_000):
        # Configure the four PWM outputs.

        if side == "left":
            self.pins = [
                PWM(Pin("GP0", Pin.OUT)),
                PWM(Pin("GP1", Pin.OUT)),
                PWM(Pin("GP2", Pin.OUT)),
                PWM(Pin("GP3", Pin.OUT)),
            ]
        elif side == "right":
            self.pins = [
                PWM(Pin("GP4", Pin.OUT)),
                PWM(Pin("GP5", Pin.OUT)),
                PWM(Pin("GP6", Pin.OUT)),
                PWM(Pin("GP7", Pin.OUT)),
            ]
        else:
            raise ValueError("side must be 'left' or 'right'")

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

        self.half_step_sequence = [
            [val, 0, 0, 0],    # Step 0
            [val, val, 0, 0],  # Step 1
            [0, val, 0, 0],    # Step 2
            [0, val, val, 0],  # Step 3
            [0, 0, val, 0],    # Step 4
            [0, 0, val, val],  # Step 5
            [0, 0, 0, val],    # Step 6
            [val, 0, 0, val],  # Step 7
        ]

        self.microstep_sequence = []
        # Keep track of the currently selected mode.
        self.current_sequence = self.full_step_sequence

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
        elif mode == "half":
            self.current_sequence = self.half_step_sequence
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
        self.set_step([0, 0, 0, 0])

    def move_stepper(self, steps, direction="forward", delay=0.01):
        if direction not in ["forward", "backward"]:
            raise ValueError("Direction must be 'forward' or 'backward'.")
        sequence = list(self.current_sequence)
        if direction == "backward":
            sequence = list(reversed(sequence))

        cycle = abs(steps) // len(sequence)

        try:
            for _ in range(cycle):
                for step in sequence:
                    self.set_step(step)
                    sleep(delay)
        finally:
            self.stop()

    def rotate_full_step(self, steps, delay):
        """Rotate through the full-step sequence."""
        sequence = self.full_step_sequence

        try:
            for _ in range(abs(steps)):
                for step in sequence:
                    self.set_step(step)
                    sleep(delay)
        finally:
            self.stop()