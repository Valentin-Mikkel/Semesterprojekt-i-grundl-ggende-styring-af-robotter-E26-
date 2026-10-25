from stepper_motor import StepperMotor
import time
import math

class DifferentialDrive:
    def __init__(self, left, right):
        """
        OTHER PARAMS?
        """
        self.left = left #get the steppermoter for each of the two
        self.right = right

        #make sure they are stopped
        self.stop()

        # some mah needed for turn and distance logic
        angle = 1.8  # angle the steppermotor turns. datablad... Fra Jes ppt
        diameter = 8  # diameter of wheels in cm

        wheelbase = 24  # distance between wheels in cm #MÅL BREDRE IKKE ENDELIGT MÅL

        circum = math.pi * diameter  # circumfrence of wheels
        turningCircum = 2 * math.pi * wheelbase  # turning circumfrance.
        stepPR = 360 / angle  # step per revolution
        self.distPS = circum / stepPR  # distance per step
        self.numStepFT = turningCircum / self.distPS  # number of steps for a full turn

    def stop(self): #stop both motors
        self.left.stop()
        self.right.stop()

    def cm_to_steps(self, distance_cm): #distance wanted to travel !!!in cm!!!
        #distTrav = self.total_steps * self.distPS  # dist travelled so far
        numberOS = distance_cm / self.distPS  # number of steps to travel
        return round(numberOS) #gives integer of number needed to turn

    def move_distance(self, distance_cm, direction, delay_us=1000):
        steps = self.cm_to_steps(distance_cm) #get amount of steps needed from function
        self.left.move_stepper(steps, direction, delay_us) #give each motor steps
        self.right.move_stepper(steps, direction, delay_us) #needs work to be in sync

    def turnMath(self, degrees): # in place rotation. degrees are degrees wanting to turn
        numStepTxD = (degrees / 360) * self.numStepFT  # number of steps to turn X degrees
        MotorSteps = numStepTxD / 2  #steps for the motors to turn x degree in place
        #otherMotorSteps = -MotorSteps  #go opposite of other motor and you'll turn
        return MotorSteps #take the negative of this for other motor

    def turn_in_place(self, degrees, direction, delay_us=1000):
        if direction == "left": #if direction is left... turn left
            self.turn_left(degrees, delay_us)
        elif direction == "right":#if direction is right... don't turn left
            self.turn_right(degrees, delay_us)
        else:
            raise ValueError("Direction must be 'left' or 'right'")
        self.stop()

    def turn_left(self, degrees, delay_us=1000):
        steps = self.turnMath(degrees) #get number of steps to turn
        self.right.move_stepper(steps, "forward", delay_us) #turn of side
        self.left.move_stepper(steps, "backward", delay_us)#needs sync

    def turn_right(self, degrees, delay_us=1000):
        steps = self.turnMath(degrees)

        self.left.move_stepper(steps, "forward", delay_us)
        self.right.move_stepper(steps, "backward", delay_us)
