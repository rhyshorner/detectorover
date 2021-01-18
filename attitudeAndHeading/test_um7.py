import um7
import time

#------------attitude calibrations------------------
rollcalibration = 0 #
pitchcalibration = 0
headingcalibration = 0

#----------initialize um7 Serial---------------------
try:
	um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200) # rpi3 serial port is /dev/ttyS0
except:
	print("um7 initialize failed.")
	print("um7 not plugged in or failed.")

#----------------read values and display-----------------
while True:
    phithetapsi = um7.rollpitchyaw()
    roll = round((phithetapsi[0] + rollcalibration), 3)
    pitch = round((phithetapsi[1] + pitchcalibration), 3)
    heading = round((phithetapsi[2] + headingcalibration), 3)
    #---- heading correction for negative values----------------
    if heading < 0:
        heading = heading + 360

    phithetapsi_rate = um7.rollpitchyaw_rate()
    roll_rate = round(phithetapsi_rate[0],3)
    pitch_rate = round(phithetapsi_rate[1], 3)
    heading_rate = round(phithetapsi_rate[2], 3)

    print("roll: " + str(roll) + ", pitch: " + str(pitch) + ", heading: " + str(heading))
    print("roll_rate: " + str(roll_rate) + ", pitch_rate: " + str(pitch_rate) + ", heading_rate: " + str(heading_rate))
    time.sleep(0.1)