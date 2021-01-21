import time

class MissionPlanner(object):
    """ miniray's mission planner script management class """
    def __init__(self, sensor_or_time_ctrl='time'):
        self.some_variable = 0
        self.countdown_timer = time.time()
        # sensor ctrl means setpoints and events are triggered by sensor outputs and given thresholds
        # time ctrl means setpoints and events are triggered only by time in seconds
        if sensor_or_time_ctrl == 'time':
            self.sensor_or_time_ctrl = 'time'
        elif sensor_or_time_ctrl == 'relative_time':
            self.sensor_or_time_ctrl = 'relative_time'
        elif sensor_or_time_ctrl == 'heading change at time':
            self.sensor_or_time_ctrl = 'heading change at time'

        # the time in seconds for each step(event)
        #eg self.mission_event_times = {'event_1':3, 'event_2':6, 'event_3':9, 'event_4':12}
        # event_1 is triggered 3 seconds after script begin
        # event_2 is triggered 6 seconds after script begin, or 3 seconds after event_1 is triggered
        self.mission_event_times = {'event_1':0, 'event_2':5, 'event_3':20, 'event_4':35}
        self.time_script_step_number = 1

    def time_script(self, pitch_trim_setpoint, roll_trim_setpoint):
        if (time.time() - self.countdown_timer) > self.mission_event_times['event_1'] and self.time_script_step_number == 1:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            roll_trim_setpoint = 0
            self.time_script_step_number = 2
            return pitch_trim_setpoint, roll_trim_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_2'] and self.time_script_step_number == 2:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 15
            roll_trim_setpoint = -15
            self.time_script_step_number = 3
            return pitch_trim_setpoint, roll_trim_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_3'] and self.time_script_step_number == 3:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = -16
            roll_trim_setpoint = 16
            self.time_script_step_number = 4
            return pitch_trim_setpoint, roll_trim_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_4'] and self.time_script_step_number == 4:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 1
            roll_trim_setpoint = 1
            self.time_script_step_number = 5
            return pitch_trim_setpoint, roll_trim_setpoint
        else:
            return pitch_trim_setpoint, roll_trim_setpoint

    def relative_time_script(self, pitch_trim_setpoint, roll_trim_setpoint):
        return pitch_trim_setpoint, roll_trim_setpoint

    def heading_change_at_time_script(self, drive_speed, heading_setpoint):
        if (time.time() - self.countdown_timer) > self.mission_event_times['event_1'] and self.time_script_step_number == 1:
            # this is where you add some modified setpoints
            drive_speed = 1
            heading_setpoint = 1
            self.time_script_step_number = 2
            return drive_speed, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_2'] and self.time_script_step_number == 2:
            # this is where you add some modified setpoints
            drive_speed = 15
            heading_setpoint = 180
            self.time_script_step_number = 3
            return drive_speed, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_3'] and self.time_script_step_number == 3:
            # this is where you add some modified setpoints
            drive_speed = -14
            heading_setpoint = 45
            self.time_script_step_number = 4
            return drive_speed, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_4'] and self.time_script_step_number == 4:
            # this is where you add some modified setpoints
            drive_speed = 2
            heading_setpoint = 2
            self.time_script_step_number = 5
            return drive_speed, heading_setpoint
        else:
            return drive_speed, heading_setpoint

    def mission_script_event_check(self, enabled, drive_speed, turn_speed, heading_setpoint):
        if enabled == 1:
            if self.sensor_or_time_ctrl == 'time':
                drive_speed, turn_speed = self.time_script(drive_speed, turn_speed)
                return drive_speed, turn_speed, heading_setpoint
            elif self.sensor_or_time_ctrl == 'relative_time':
                drive_speed, turn_speed = self.relative_time_script(drive_speed, turn_speed)
                return drive_speed, turn_speed, heading_setpoint
            elif self.sensor_or_time_ctrl == 'heading change at time':
                drive_speed, heading_setpoint = self.heading_change_at_time_script(drive_speed, heading_setpoint)
                return drive_speed, turn_speed, heading_setpoint
        else:
            self.time_script_step_number = 1
            self.countdown_timer = time.time()
            return drive_speed, turn_speed, heading_setpoint