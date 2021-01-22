# a class to manage the drive and steering system
import board
import busio
from adafruit_servokit import ServoKit
import time

class DriveSystem(object):
    """ detectorover's forward drive and steering management class """
    def __init__(self, min_drive_speed, max_drive_speed, min_turn_speed, max_turn_speed):
        self.i2c = busio.I2C(board.SCL, board.SDA) #initialize i2c on rpi
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].set_pulse_width_range(0, 19988) # for LHS input3
        self.kit.servo[1].set_pulse_width_range(0, 19988) # for LHS input4
        self.kit.servo[2].set_pulse_width_range(0, 19988) # for LHS enableB
        self.kit.servo[3].set_pulse_width_range(0, 19988) # for RHS input3
        self.kit.servo[4].set_pulse_width_range(0, 19988) # for RHS input4
        self.kit.servo[5].set_pulse_width_range(0, 19988) # for RHS enableA

        self.min_drive_speed = min_drive_speed        
        self.max_drive_speed = max_drive_speed
        self.min_turn_speed = min_turn_speed
        self.max_turn_speed = min_turn_speed

        self.LHS_forward_power = 0 # power given equally to LHS motors
        self.RHS_forward_power = 0 # power given equally to LHS motors
        self.turn_power = 0 # power difference given to LHS and RHS motors

    def drive(self, enabled, speed):
        if enabled == 1:
            if speed > 0:
                self.kit.servo[2].angle = speed
                self.kit.servo[0].angle = 180
            if speed < 0:
                self.kit.servo[2].angle = -speed
                self.kit.servo[0].angle = 0
                self.kit.servo[1].angle = 180
            elif speed == 0:
                self.kit.servo[2].angle = 0
                self.kit.servo[0].angle = 0
                self.kit.servo[1].angle = 0 
        else:
            self.kit.servo[2].angle = 0
            self.kit.servo[0].angle = 0
            self.kit.servo[1].angle = 0
        return

    def turn(self, enabled, speed):
        return

# kit.servo[1].angle = 180 # move channel 1 to 180 degress
# # for controlling LEDS
# pwm_controller.frequency = 60 # make frequency of pwm_controller 60hz
# led_channel = pwm_controller.channels[0] #name a channel for easier reference
# led_channel.duty_cycle = 0xffff # set led pwm to 0xffff, or full or 65535, duty cycle
# led_channel.duty_cycle = 0 # set off
# led_channel.duty_cycle = 1000 #set middle roughly

