import time
import numpy as np
from icm20948 import ICM20948
from kalman import Kalman
import csv

imu = ICM20948()
sensorfusion = Kalman()

imu.read_sensors()
imu.computeOrientation()
sensorfusion.roll = imu.roll
sensorfusion.pitch = imu.pitch
sensorfusion.yaw = imu.yaw

currTime = time.time()

while True:
    imu.read_sensors()
    imu.computeOrientation()

    print("roll: " + str(imu.roll) + ", pitch: " + str(imu.pitch) + ", yaw: " + str(imu.yaw))
    
    newTime = time.time()
    dt = newTime - currTime
    currTime = newTime

    sensorfusion.computeAndUpdateRollPitchYaw(imu.accel_data[0], imu.accel_data[1], imu.accel_data[2], imu.gyro_data[0], imu.gyro_data[1], imu.gyro_data[2],imu.magneto_data[0], imu.magneto_data[1], imu.magneto_data[2], dt)

    print("kalman roll: " + str(sensorfusion.roll) + ", kalman pitch: " + str(sensorfusion.pitch) + ", kalman yaw: " + str(sensorfusion.yaw) + ", delta_time: " + str(dt))

    #time.sleep(0.1)
