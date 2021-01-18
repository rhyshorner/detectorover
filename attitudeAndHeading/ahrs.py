from . import um7

class Um7Ahrs(object):
    """ miniray's attitude and heading management class """
    def __init__(self):
        self.um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200) # rpi3 serial port is /dev/ttyS0
        self.roll_pitch_yaw = {}
        pass

    def request_rollpitchyaw(self):
        rollpitchyaw = self.um7.rollpitchyaw()
        #if rollpitchyaw[2] < 0:
        #   rollpitchyaw[2] = rollpitchyaw[2] + 360
        self.roll_pitch_yaw = {'roll':rollpitchyaw[0], 'pitch':rollpitchyaw[1], 'heading':rollpitchyaw[2]}
        return self.roll_pitch_yaw

    def request_rollpitchyaw_list(self):
        rollpitchyaw = self.um7.rollpitchyaw()
        if rollpitchyaw[2] < 0:
           rollpitchyaw[2] = rollpitchyaw[2] + 360
        return rollpitchyaw

    def request_rollpitchyaw_rate_list(self):
        rollpitchyaw = self.um7.rollpitchyaw_rate()
        return rollpitchyaw