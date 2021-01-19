# a class to manage the drive and steering system
import board
import busio
from adafruit_servokit import ServoKit



class DriveSystem(object):
    """ detectorover's forward drive and steering management class """
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA) #initialize i2c on rpi
        self.pwm_controller = adafruit_pca9685.PCA9685(i2c) #create instance of PCA9685 class
        #self.um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200) # rpi3 serial port is /dev/ttyS0
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[1].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[2].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[3].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[4].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[5].set_pulse_width_range(0, 19988) # for LHS
        self.kit.servo[16].set_pulse_width_range(1000, 2000) # an example for ordinary servo

        kit.servo[1].angle = 180 # move channel 1 to 180 degress
        kit.servo[1].angle = 0 # move channel 1 to 0 degress
        self.LHS_forward_power = 0 # power given equally to LHS motors
        self.RHS_forward_power = 0 # power given equally to LHS motors
        self.directional_power = 0 # power difference given to LHS and RHS motors




# # for controlling LEDS
# pwm_controller.frequency = 60 # make frequency of pwm_controller 60hz
# led_channel = pwm_controller.channels[0] #name a channel for easier reference
# led_channel.duty_cycle = 0xffff # set led pwm to 0xffff, or full or 65535, duty cycle
# led_channel.duty_cycle = 0 # set off
# led_channel.duty_cycle = 1000 #set middle roughly

