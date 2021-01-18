from . import pid

class HeadingController(object):
    """ class for operating heading control  """
    def __init__(self, proportional_gain, intergral_gain, derivative_gain, maximum_roll):
        self.pid = pid.PID(P=proportional_gain,I=intergral_gain,D=derivative_gain)
        self.pid.setSampleTime(sample_time=0.03)
        self.maximum_roll = maximum_roll


    def control_loop(self, enabled, heading_setpoint, current_heading, current_roll_setpoint): 
        heading_error, roll_angle_output, PTerm, ITerm, DTerm = self.pid.update(heading_setpoint, current_heading)
        if enabled == 1:
            # restrict maximum roll_angle_output
            if roll_angle_output > self.maximum_roll:
                roll_angle_output = self.maximum_roll
            elif roll_angle_output <= -self.maximum_roll:
                roll_angle_output = -self.maximum_roll
        else:
            roll_angle_output = current_roll_setpoint # disabled, motor off
        return round(heading_error,3), round(roll_angle_output,3), round(PTerm,3), round(ITerm,3), round(DTerm,3)

#df['heading_ctrl_error'], df['heading_ctrl_output'], df['roll_trim_setpoint'], df['heading_ctrl_Pterm'], df['heading_ctrl_Iterm'], df['heading_ctrl_Dterm']