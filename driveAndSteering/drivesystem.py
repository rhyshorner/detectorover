# a class to manage the drive and steering system
import board
import busio
from adafruit_servokit import ServoKit
import time


class DriveSystem(object):
    """ detectorover's forward drive and steering management class """
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA) #initialize i2c on rpi
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[1].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[2].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[3].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[4].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[5].set_pulse_width_range(0, 19988) # for LHS

        self.LHS_forward_power = 0 # power given equally to LHS motors
        self.RHS_forward_power = 0 # power given equally to LHS motors
        self.turn_power = 0 # power difference given to LHS and RHS motors
        self.currently_driving_countdown_flag = 0
        self.currently_turning_countdown_flag = 0
        self.driving_countdown_timer = time.time()
        self.driving_countdown = 0
        self.turning_countdown_timer = time.time()
        self.turning_countdown = 0

    def drive(self, enabled, speed, amount_of_time):
        return

    def turn(self, enabled, speed, amount_of_time):
        return



# kit.servo[1].angle = 180 # move channel 1 to 180 degress
# # for controlling LEDS
# pwm_controller.frequency = 60 # make frequency of pwm_controller 60hz
# led_channel = pwm_controller.channels[0] #name a channel for easier reference
# led_channel.duty_cycle = 0xffff # set led pwm to 0xffff, or full or 65535, duty cycle
# led_channel.duty_cycle = 0 # set off
# led_channel.duty_cycle = 1000 #set middle roughly

