from .icm20948 import ICM20948
from .kalman import Kalman
import time

class Ahrs(object):
    """ detectorovers's attitude and heading management class """
    def __init__(self):
        self.imu = ICM20948()
        self.sensorfusion = Kalman()

        self.imu.read_sensors()
        self.imu.computeOrientation()
        self.roll_pitch_yaw = [0,0,0]

        self.currTime = time.time()
        pass

    def roll_pitch_yaw_kalman(self):
        newTime = time.time()
        dt = newTime - self.currTime
        self.currTime = newTime

        self.imu.read_sensors()
        self.sensorfusion.computeAndUpdateRollPitchYaw(
            self.imu.accel_data[0], self.imu.accel_data[1], self.imu.accel_data[2], 
            self.imu.gyro_data[0], self.imu.gyro_data[1], self.imu.gyro_data[2],self.imu.magneto_data[0], self.imu.magneto_data[1], 
            self.imu.magneto_data[2], dt)
        self.roll_pitch_yaw = [self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw]
        return self.roll_pitch_yaw