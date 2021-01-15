import RPi.GPIO as GPIO  
import board
import busio
import adafruit_pca9685        
from time import sleep
from adafruit_servokit import ServoKit

class TrimSystem(object):
    """ class for driving 4wheel motors  """
    def __init__(self):
        self.rear_Rwheel_in1 = 1 #GPIO?
        self.rear_Rwheel_in2 = 1 #GPIO?
        self.rear_Lwheel_in3 = 17 #GPIO17
        self.rear_Lwheel_in4 = 27 #GPIO27
        self.fore_Lwheel_channel = 1 # servo hat channel
        self.fore_Rwheel_channel = 2 # servo hat channel
        self.rear_Lwheel_channel = 3 # servo hat channel
        self.rear_Rwheel_channel = 4 # servo hat channel

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rear_Lwheel_in3,GPIO.OUT)
        GPIO.setup(self.rear_Lwheel_in4,GPIO.OUT)
        GPIO.output(self.rear_Lwheel_in3,GPIO.LOW)
        GPIO.output(self.rear_Lwheel_in4,GPIO.LOW)

        # for controlling servos
        self.servo_kit = ServoKit(channels=16, frequency=50)
        self.servo_kit.servo[self.rear_Lwheel_channel].set_pulse_width_range(0, 19988) # for led
        #kit.servo[0].set_pulse_width_range(1000, 2000) # for servo

    def set_motor_speed(self, channel, speed):
        self.servo_kit.servo[channel].angle = speed
        return speed