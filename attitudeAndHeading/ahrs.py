from . import mpu6050

class Mpu6050Ahrs(object):
    """ miniray's attitude and heading management class """
    def __init__(self):
        self.um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200) # rpi3 serial port is /dev/ttyS0
        pass

    def request_rollpitch_list(self):
        return rollpitch

    def request_rollpitch_rate_list(self):
        return rollpitch