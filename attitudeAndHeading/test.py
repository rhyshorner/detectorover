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

    print(f"roll: {round(imu.roll,3)}, pitch: {round(imu.pitch,3)}, yaw: {round(imu.yaw,3)}")
    
    newTime = time.time()
    dt = newTime - currTime
    currTime = newTime

    sensorfusion.computeAndUpdateRollPitchYaw(
        imu.accel_data[0], imu.accel_data[1], imu.accel_data[2], 
        imu.gyro_data[0], imu.gyro_data[1], imu.gyro_data[2],imu.magneto_data[0], imu.magneto_data[1], 
        imu.magneto_data[2], dt)

    print(f"kalman roll: {round(sensorfusion.roll,3)}, kalman pitch: {round(sensorfusion.pitch,3)}, kalman yaw: {round(sensorfusion.yaw,3)}, delta_time: {round(dt,3)}")

    #time.sleep(0.1)
