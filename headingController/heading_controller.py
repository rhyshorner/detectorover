from . import pid

class HeadingController(object):
    """ class for operating heading control  """
    def __init__(self, proportional_gain, intergral_gain, derivative_gain, maximum_turn_speed):
        self.pid = pid.PID(P=proportional_gain,I=intergral_gain,D=derivative_gain)
        self.pid.setSampleTime(sample_time=0.03)
        self.maximum_turn_speed = maximum_turn_speed


    def control_loop(self, enabled, heading_setpoint, current_heading, current_turning_setpoint): 
        heading_error, PID_output, PTerm, ITerm, DTerm = self.pid.update(heading_setpoint, current_heading)
        if enabled == 1:
            # restrict maximum PID_output
            if PID_output > self.maximum_turn_speed:
                PID_output = self.maximum_turn_speed
            elif PID_output <= -self.maximum_turn_speed:
                PID_output = -self.maximum_turn_speed
        else:
            PID_output = current_turning_setpoint # disabled, motor off
        return round(heading_error,3), round(PID_output,3), round(PTerm,3), round(ITerm,3), round(DTerm,3)