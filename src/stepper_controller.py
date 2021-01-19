import RPi.GPIO as GPIO
import time

class StepperController():
    def __init__(self, step_delay_ms=2, move_steps=80): 
        self.step_delay = int(step_delay_ms) / 1000 # Convert ms to seconds
        
        self.move_steps = move_steps # Number of steps move in each direction

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.coil_A_1_pin = 4 # pink
        self.coil_A_2_pin = 17 # orange
        self.coil_B_1_pin = 23 # blue
        self.coil_B_2_pin = 24 # yellow
 
        # adjust if different
        self.step_count = 4
        self.seq = list(range(0, self.step_count))
        self.seq[0] = [1,0,0,0]
        self.seq[1] = [0,1,0,0]
        self.seq[2] = [0,0,1,0]
        self.seq[3] = [0,0,0,1]
 
        #Enable output pins
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

    def __set_step(self, w1, w2, w3, w4):
        """Make one step"""
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)
 
    def forward(self):
        for i in range(self.move_steps):
            for j in range(self.step_count):
                self.__set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(self.step_delay)
 
    def backward(self):
        for i in range(self.move_steps):
            for j in reversed(range(self.step_count)):
                self.__set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(self.step_delay)
 
if __name__ == '__main__':
    sc = StepperController()
    while True:
        print("Going forward")
        sc.forward()
        time.sleep(5)
        print("Going backward")
        sc.backward()
        time.sleep(5)