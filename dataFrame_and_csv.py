# will have variables changes to suit detectorover

import time
import datetime
import csv

def create_dataframe():
    df = {
    # time and timing
    'loop_count':0,
    'loop_speed':0,
    'SBC_powered_up_time':round(time.perf_counter(),2),
    # sensors, instruments and calculated sensory data
    'pressure_mbar':0,
    'vertical_speed':0,
    'depth_m_MSL':0,
    'depth_m_local_pressure':0,
    'water_temperature_c':0,
    'roll_AHRS_deg':0,
    'pitch_AHRS_deg':0,
    'heading_AHRS_deg':0,
    'roll_rate_AHRS_deg':0,
    'pitch_rate_AHRS_deg':0,
    'heading_rate_AHRS_deg':0,
    'vertical_speed_mps':0,
    'turn_rate_dpm':0,
    # sub-system enable and disable-------------------------------------------------------
    'heading_controller_enable':0, # if enabled will override !GUI roll Setpoint! 
    'roll_trim_enable':0, # bit controls whether the roll trim is on
    'pitch_trim_enable':0, # bit controls whether the pitch trim is on
    'csv_logging_enable':0, # a configurable setting
    'drop_weight_control_enable':0, # a configurable setting
    'gui_enabled':0, # this bit enables the GUI pitch/roll setpionts. GUI opens and displays data still
    'mission_script_enabled':0, # setpoints will be chosen by mission_planner, GUI setpoint will override this if enabled.
    'mission_script_type':'heading change at time', # time, relative_time, depth, sensor, heading change at time, heading change at depth
    'live_graph_csv_enable':0, # enables a 2nd csv file to be create and opened with PIDterm_graph.py 
    #--------------------------------------------------------------------------------------
    # calibration and offsets
    'roll_calibration_AHRS_deg':0, # a configurable setting
    'pitch_calibration_AHRS_deg':0, # a configurable setting
    'heading_calibration_AHRS_deg':0, # a configurable setting
    # user configurations and auxillary information
    'heading_setpoint':0, # not currently used but implementation in progress.
    'roll_trim_setpoint':0, # 
    'pitch_trim_setpoint':0, # 
    'drop_weight_depth_setpoint':0, # not implemented yet
    # Control surfaces and actuators
    #heading
    'heading_ctrl_error':0, # current heading - heading setpoint
    'heading_ctrl_P_gain':0.25, # a configurable setting
    'heading_ctrl_I_gain':0,
    'heading_ctrl_D_gain':0,
    'heading_ctrl_Pterm':0, # Proportional error
    'heading_ctrl_Iterm':0, # Integral error
    'heading_ctrl_Dterm':0, # Derivative error
    #roll
    'roll_trim_current_position':0,
    'roll_trim_output':0,
    'roll_trim_velocity':0,
    'roll_trim_certainty':'uncertain',
    'roll_trim_Vin':0,
    'roll_trim_error':0,
    'roll_trim_P_gain':75, # a configurable setting
    'roll_trim_I_gain':0,
    'roll_trim_D_gain':35,
    'roll_trim_Pterm':0, # returned from PID calculations
    'roll_trim_Iterm':0, # returned from PID calculations
    'roll_trim_Dterm':0, # returned from PID calculations
    #pitch
    'pitch_trim_current_position':0,
    'pitch_trim_output':0,
    'pitch_trim_velocity':0,
    'pitch_trim_certainty':'uncertain',
    'pitch_trim_Vin':0,
    'pitch_trim_error':0,
    'pitch_trim_P_gain':75,#75 gain in water # a configurable setting #15 gain in air
    'pitch_trim_I_gain':0,
    'pitch_trim_D_gain':35,#35 gain in water #-55 gain in air
    'pitch_trim_Pterm':0, # returned from PID calculations
    'pitch_trim_Iterm':0, # returned from PID calculations
    'pitch_trim_Dterm':0, # returned from PID calculations
    #dropweight
    'drop_weight_triggered':0,
    #maximum and minimum constraints
    'maximum_roll':25,
    }
    return df

def update_df(df, window1, roll_trim_system, ahrs_instrument, pitch_trim_system, pressuresensor):
    df['loop_count'] = df['loop_count'] + 1
    df['loop_speed'] = round(time.perf_counter() - df['SBC_powered_up_time'],3)
    df['SBC_powered_up_time'] = round(time.perf_counter(),3)

    df['gui_enabled'] = window1.gui_enabled_intvar.get()
    df['heading_controller_enable'] = window1.heading_controller_enable_intvar.get()
    df['roll_trim_enable'] = window1.roll_trim_enable_intvar.get()
    df['pitch_trim_enable'] = window1.pitch_trim_enable_intvar.get()
    df['csv_logging_enable'] = window1.csv_logging_enable_intvar.get()
    df['drop_weight_control_enable'] = window1.drop_weight_control_enable_intvar.get()
    df['mission_script_enabled'] = window1.mission_script_enabled_intvar.get()
    df['live_graph_csv_enable'] = window1.live_graph_enabled_intvar.get()

    try:
        df['pressure_mbar'] = round(pressuresensor.pressure_mbar(),3)
        df['vertical_speed'] = round(pressuresensor.vertical_speed_estimate(),3)
        df['depth_m_MSL'] = round(pressuresensor.depth_meters_MSL(),3)
        df['depth_m_local_pressure'] = round(pressuresensor.depth_meters(),3)
        df['water_temperature_c'] = round(pressuresensor.sensor_temperature(),3)
    except:
        df['pressure_mbar'] = df['pressure_mbar']
        df['vertical_speed'] = df['vertical_speed']
        df['depth_m_MSL'] = df['depth_m_MSL']
        df['depth_m_local_pressure'] = df['depth_m_local_pressure']
        df['water_temperature_c'] = df['water_temperature_c']
        print("!!!! pressure sensor threw exception !!!!")
    
    try:
        AHRS_list = ahrs_instrument.request_rollpitchyaw_list()
        df['roll_AHRS_deg'] = round(AHRS_list[0],3)
        df['pitch_AHRS_deg'] = round(AHRS_list[1],3)
        df['heading_AHRS_deg'] = round(AHRS_list[2],3)
    except:
        df['roll_AHRS_deg'] = df['roll_AHRS_deg']
        df['pitch_AHRS_deg'] = df['pitch_AHRS_deg']
        df['heading_AHRS_deg'] = df['heading_AHRS_deg']
        print("!!!! um7 sensor threw exception !!!!")
    try:
        AHRS_rate_list = ahrs_instrument.request_rollpitchyaw_rate_list()
        df['roll_rate_AHRS_deg'] = round(AHRS_rate_list[0],3)
        df['pitch_rate_AHRS_deg'] = round(AHRS_rate_list[1],3)
        df['heading_rate_AHRS_deg'] = round(AHRS_rate_list[2],3)
    except:
        df['roll_rate_AHRS_deg'] = df['roll_rate_AHRS_deg']
        df['pitch_rate_AHRS_deg'] = df['pitch_rate_AHRS_deg']
        df['heading_rate_AHRS_deg'] = df['heading_rate_AHRS_deg']
        print("!!!! um7 sensor threw exception !!!!")

    if df['gui_enabled'] == 1:
        df['heading_setpoint'] = window1.heading_intvar.get()
        df['roll_trim_setpoint'] = window1.roll_trim_intvar.get()
        df['pitch_trim_setpoint'] = window1.pitch_trim_intvar.get()
    else:
        df['heading_setpoint'] = df['heading_setpoint']
        df['roll_trim_setpoint'] = df['roll_trim_setpoint']
        df['pitch_trim_setpoint'] = df['pitch_trim_setpoint']

    df['roll_trim_current_position'] = roll_trim_system.get_position()
    df['roll_trim_certainty'] = roll_trim_system.get_position_certainty()
    df['roll_trim_Vin'] = roll_trim_system.get_Vin()
    df['pitch_trim_current_position'] = pitch_trim_system.get_position()
    df['pitch_trim_certainty'] = pitch_trim_system.get_position_certainty()
    df['pitch_trim_Vin'] = pitch_trim_system.get_Vin()
    return df

def create_main_csv(df):
    if df['csv_logging_enable'] == 1:
        filetimestamp = "{:%H-%M-%S_%Y-%m-%d}".format(datetime.datetime.now())
        csvfilename = "./loggedData/" + filetimestamp + "_miniray.csv"
        f = open(csvfilename, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(list(df.keys()))
        f.close()
        return csvfilename

def create_new_graph_csv_row(df):
    if df['live_graph_csv_enable'] == 1:
        graph_csvfilename = "./loggedData/data.csv"
        f = open(graph_csvfilename, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(list(df.keys()))
        f.close()
        return graph_csvfilename

def write_new_csv_row(df, csvfilename):
    if df['csv_logging_enable'] == 1:
        with open(csvfilename, mode='a', newline='') as f:
            csv.writer(f, delimiter=',').writerow(list(df.values()))
            f.close()
    return

def write_new_graph_csv_row(df, graph_csvfilename):
    if df['live_graph_csv_enable'] == 1:
        with open(graph_csvfilename, mode='a', newline='') as f:
            csv.writer(f, delimiter=',').writerow(list(df.values()))
            f.close()
    return