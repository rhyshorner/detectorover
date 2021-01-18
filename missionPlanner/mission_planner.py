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
        elif sensor_or_time_ctrl == 'depth':
            self.sensor_or_time_ctrl = 'depth'
        elif sensor_or_time_ctrl == 'sensor':
            self.sensor_or_time_ctrl = 'sensor'
        elif sensor_or_time_ctrl == 'heading change at depth':
            self.sensor_or_time_ctrl = 'heading change at depth'
        elif sensor_or_time_ctrl == 'heading change at time':
            self.sensor_or_time_ctrl = 'heading change at time'

        # the time in seconds for each step(event)
        #eg self.mission_event_times = {'event_1':3, 'event_2':6, 'event_3':9, 'event_4':12}
        # event_1 is triggered 3 seconds after script begin
        # event_2 is triggered 6 seconds after script begin, or 3 seconds after event_1 is triggered
        self.mission_event_times = {'event_1':0, 'event_2':5, 'event_3':20, 'event_4':35}
        self.time_script_step_number = 1
        # depth reached for each event, in meters then trigger setpoint change
        self.mission_event_depths = {'depth_1':0.5, 'depth_2':4, 'depth_3': 5.5}
        self.depth_script_step_number = 1

    def sensor_script(self, df):
        # if specific depth or other sensor condition reached then modify setpoints and events
        return df

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

    def depth_script(self, depth, pitch_trim_setpoint, roll_trim_setpoint):
        if depth >= self.mission_event_depths['depth_1'] and self.depth_script_step_number == 1:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            roll_trim_setpoint = 15
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 2
            return pitch_trim_setpoint, roll_trim_setpoint
        elif depth >= self.mission_event_depths['depth_2'] and self.depth_script_step_number == 2:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            roll_trim_setpoint = -15
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 3
            return pitch_trim_setpoint, roll_trim_setpoint
        elif depth >= self.mission_event_depths['depth_3'] and self.depth_script_step_number == 3:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            roll_trim_setpoint = 0
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 4
            return pitch_trim_setpoint, roll_trim_setpoint
        else:
            return pitch_trim_setpoint, roll_trim_setpoint

    def heading_change_at_depth_script(self, depth, pitch_trim_setpoint, heading_setpoint):
        if depth >= self.mission_event_depths['depth_1'] and self.depth_script_step_number == 1:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            heading_setpoint = 45
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 2
            return pitch_trim_setpoint, roll_trim_setpoint
        elif depth >= self.mission_event_depths['depth_2'] and self.depth_script_step_number == 2:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            heading_setpoint = -45
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 3
            return pitch_trim_setpoint, roll_trim_setpoint
        elif depth >= self.mission_event_depths['depth_3'] and self.depth_script_step_number == 3:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 0
            heading_setpoint = 0
            #increment step_numnber so not to set setpoints again later on.
            self.depth_script_step_number = 4
            return pitch_trim_setpoint, heading_setpoint
        else:
            return pitch_trim_setpoint, heading_setpoint

    def heading_change_at_time_script(self, pitch_trim_setpoint, heading_setpoint):
        if (time.time() - self.countdown_timer) > self.mission_event_times['event_1'] and self.time_script_step_number == 1:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 1
            heading_setpoint = 1
            self.time_script_step_number = 2
            return pitch_trim_setpoint, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_2'] and self.time_script_step_number == 2:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 15
            heading_setpoint = 180
            self.time_script_step_number = 3
            return pitch_trim_setpoint, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_3'] and self.time_script_step_number == 3:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = -14
            heading_setpoint = 45
            self.time_script_step_number = 4
            return pitch_trim_setpoint, heading_setpoint
        elif (time.time() - self.countdown_timer) > self.mission_event_times['event_4'] and self.time_script_step_number == 4:
            # this is where you add some modified setpoints
            pitch_trim_setpoint = 2
            heading_setpoint = 2
            self.time_script_step_number = 5
            return pitch_trim_setpoint, heading_setpoint
        else:
            return pitch_trim_setpoint, heading_setpoint

    def mission_script_event_check(self, enabled, depth, pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint):
        if enabled == 1:
            if self.sensor_or_time_ctrl == 'sensor':
                pitch_trim_setpoint, roll_trim_setpoint = self.sensor_script(pitch_trim_setpoint, roll_trim_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
            elif self.sensor_or_time_ctrl == 'time':
                pitch_trim_setpoint, roll_trim_setpoint = self.time_script(pitch_trim_setpoint, roll_trim_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
            elif self.sensor_or_time_ctrl == 'relative_time':
                pitch_trim_setpoint, roll_trim_setpoint = self.relative_time_script(pitch_trim_setpoint, roll_trim_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
            elif self.sensor_or_time_ctrl == 'depth':
                pitch_trim_setpoint, roll_trim_setpoint = self.depth_script(depth, pitch_trim_setpoint, roll_trim_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
            elif self.sensor_or_time_ctrl == 'heading change at depth':
                pitch_trim_setpoint, heading_setpoint = self.heading_change_at_depth_script(depth, pitch_trim_setpoint, heading_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
            elif self.sensor_or_time_ctrl == 'heading change at time':
                pitch_trim_setpoint, heading_setpoint = self.heading_change_at_time_script(pitch_trim_setpoint, heading_setpoint)
                return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint
        else:
            self.time_script_step_number = 1
            self.depth_script_step_number = 1
            self.countdown_timer = time.time()
            return pitch_trim_setpoint, roll_trim_setpoint, heading_setpoint