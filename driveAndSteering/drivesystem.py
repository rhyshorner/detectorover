# a class to manage the drive and steering system
import board
import busio
from adafruit_servokit import ServoKit
import time

class DriveSystem(object):
    """ detectorover's component level drive/steering controller class """
    def __init__(self, min_motor_speed, max_motor_speed):
        self.i2c = busio.I2C(board.SCL, board.SDA) #initialize i2c on rpi
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].set_pulse_width_range(0, 19988) # for LHS input3
        self.kit.servo[1].set_pulse_width_range(0, 19988) # for LHS input4
        self.kit.servo[2].set_pulse_width_range(0, 19988) # for LHS enableB
        self.kit.servo[3].set_pulse_width_range(0, 19988) # for RHS input3
        self.kit.servo[4].set_pulse_width_range(0, 19988) # for RHS input4
        self.kit.servo[5].set_pulse_width_range(0, 19988) # for RHS enableA

        self.min_motor_speed = min_motor_speed        
        self.max_motor_speed = max_motor_speed

        self.LHS_drive_power = 0 # power given equally to LHS motors
        self.RHS_drive_power = 0 # power given equally to RHS motors
        self.turn_power = 0 # power difference given to LHS and RHS motors

    def drive(self, enabled, speed, turn):
        if enabled == 1:
            self.LHS_drive_power = speed + turn
            self.RHS_drive_power = speed - turn

            if self.LHS_drive_power > self.max_motor_speed:
                self.LHS_drive_power = self.max_motor_speed
            elif self.LHS_drive_power < -self.max_motor_speed:
                self.LHS_drive_power = -self.max_motor_speed
            elif self.LHS_drive_power > 0 and self.LHS_drive_power < self.min_motor_speed:
                self.LHS_drive_power = self.min_motor_speed
            elif self.LHS_drive_power < 0 and self.LHS_drive_power > -self.min_motor_speed: 
                self.LHS_drive_power = -self.min_motor_speed

            if self.RHS_drive_power > self.max_motor_speed:
                self.RHS_drive_power = self.max_motor_speed
            elif self.RHS_drive_power < -self.max_motor_speed:
                self.RHS_drive_power = -self.max_motor_speed
            elif self.RHS_drive_power > 0 and self.RHS_drive_power < self.min_motor_speed:
                self.RHS_drive_power = self.min_motor_speed
            elif self.RHS_drive_power < 0 and self.RHS_drive_power > -self.min_motor_speed: 
                self.RHS_drive_power = -self.min_motor_speed

            if self.LHS_drive_power > 0:
                self.kit.servo[2].angle = self.LHS_drive_power
                self.kit.servo[0].angle = 180
                self.kit.servo[1].angle = 0
            elif self.LHS_drive_power < 0:
                self.kit.servo[2].angle = -self.LHS_drive_power
                self.kit.servo[0].angle = 0
                self.kit.servo[1].angle = 180
            elif self.LHS_drive_power == 0:
                self.kit.servo[2].angle = 0
                self.kit.servo[0].angle = 0
                self.kit.servo[1].angle = 0

            if self.RHS_drive_power > 0:
                self.kit.servo[5].angle = self.RHS_drive_power
                self.kit.servo[3].angle = 180
                self.kit.servo[4].angle = 0
            elif self.RHS_drive_power < 0:
                self.kit.servo[5].angle = -self.RHS_drive_power
                self.kit.servo[3].angle = 0
                self.kit.servo[4].angle = 180
            elif self.RHS_drive_power == 0:
                self.kit.servo[5].angle = 0
                self.kit.servo[3].angle = 0
                self.kit.servo[4].angle = 0

        else:
            self.LHS_drive_power = self.LHS_drive_power
            self.RHS_drive_power = self.RHS_drive_power
            self.kit.servo[2].angle = 0
            self.kit.servo[0].angle = 0
            self.kit.servo[1].angle = 0
        return self.LHS_drive_power, self.RHS_drive_power

    def turn(self, enabled, speed):
        return

# kit.servo[1].angle = 180 # move channel 1 to 180 degress
# # for controlling LEDS
# pwm_controller.frequency = 60 # make frequency of pwm_controller 60hz
# led_channel = pwm_controller.channels[0] #name a channel for easier reference
# led_channel.duty_cycle = 0xffff # set led pwm to 0xffff, or full or 65535, duty cycle
# led_channel.duty_cycle = 0 # set off
# led_channel.duty_cycle = 1000 #set middle roughly

