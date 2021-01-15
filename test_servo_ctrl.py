import board
import busio
import adafruit_pca9685


# for controlling LEDS
i2c = busio.I2C(board.SCL, board.SDA) #initialize i2c on rpi
pwm_controller = adafruit_pca9685.PCA9685(i2c) #create instance of PCA9685 class

pwm_controller.frequency = 60 # make frequency of pwm_controller 60hz
led_channel = pwm_controller.channels[0] #name a channel for easier reference
led_channel.duty_cycle = 0xffff # set led pwm to 0xffff, or full or 65535, duty cycle
led_channel.duty_cycle = 0 # set off
led_channel.duty_cycle = 1000 #set middle roughly

# for controlling servos
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[1].angle = 180 # move channel 1 to 180 degress
kit.servo[1].angle = 0 # move channel 1 to 0 degress