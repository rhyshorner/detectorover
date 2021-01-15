import RPi.GPIO as GPIO          
from time import sleep

in3 = 17
in4 = 27
enB = 13
temp1=1

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

forward
in3=HIGH
in4=LOW

reverse 
in3=LOW
in4=HIGH

Stop
in3=LOW
in4=LOW

