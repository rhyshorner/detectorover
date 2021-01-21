# will have variables changes to suit detectorover

import time
import datetime
import csv

def create_dataframe():
    df = {
    # time and timing
    'loop_count':0,
    'loop_speed':0,
    'current_time':'{:%H-%M-%S}'.format(datetime.datetime.now()),
    'SBC_powered_up_time':round(time.perf_counter(),2),
    # sensors, instruments and calculated sensory data
    'pressure_mbar':0,
    'altitude_MSL':0,
    'altitude_local_pressure':0,
    'pressure_sensor_temperature_c':0,
    'roll_AHRS_deg':0,
    'pitch_AHRS_deg':0,
    'heading_AHRS_deg':0,
    'roll_rate_AHRS_deg':0,
    'pitch_rate_AHRS_deg':0,
    'heading_rate_AHRS_deg':0,
    # sub-system enable and disable-------------------------------------------------------
    'heading_controller_enable':0, # if enabled will override !GUI roll Setpoint! 
    'drive_enable':0, # bit controls whether the roll trim is on
    'turn_enable':0, # bit controls whether the pitch trim is on
    'csv_logging_enable':0, # a configurable setting
    'gui_enabled':0, # this bit enables the GUI pitch/roll setpionts. GUI opens and displays data still
    'mission_script_enabled':0, # setpoints will be chosen by mission_planner, GUI setpoint will override this if enabled.
    'mission_script_type':'heading change at time', # time, relative_time, depth, sensor, heading change at time, heading change at depth
    #--------------------------------------------------------------------------------------
    # calibration and offsets
    'roll_calibration_AHRS_deg':0, # a configurable setting
    'pitch_calibration_AHRS_deg':0, # a configurable setting
    'heading_calibration_AHRS_deg':0, # a configurable setting
    # drive and turning variables
    'heading_setpoint':0, # variable to control heading
    'drive_speed':0, # variable to set the motor driver PWM, a negative number is reverse
    'turn_speed':0, # 
    # Control surfaces and actuators
    #heading
    'heading_ctrl_error':0, # current heading - heading setpoint
    'heading_ctrl_P_gain':0.25, # a configurable setting
    'heading_ctrl_I_gain':0,
    'heading_ctrl_D_gain':0,
    'heading_ctrl_Pterm':0, # Proportional error
    'heading_ctrl_Iterm':0, # Integral error
    'heading_ctrl_Dterm':0, # Derivative error
    # for future to drive with encoder feedback motors
    # LHS
    'LHS_motor_current_speed':0,
    'LHS_motor_output':0,
    'LHS_motor_velocity':0,
    'LHS_motor_error':0,
    'LHS_motor_P_gain':75, # a configurable setting
    'LHS_motor_I_gain':0, # a configurable setting
    'LHS_motor_D_gain':35, # a configurable setting
    'LHS_motor_Pterm':0, # returned from PID calculations
    'LHS_motor_Iterm':0, # returned from PID calculations
    'LHS_motor_Dterm':0, # returned from PID calculations
    # RHS
    'RHS_motor_current_speed':0,
    'RHS_motor_output':0,
    'RHS_motor_velocity':0,
    'RHS_motor_error':0,
    'RHS_motor_P_gain':75, # a configurable setting
    'RHS_motor_I_gain':0, # a configurable setting
    'RHS_motor_D_gain':35, # a configurable setting
    'RHS_motor_Pterm':0, # returned from PID calculations
    'RHS_motor_Iterm':0, # returned from PID calculations
    'RHS_motor_Dterm':0, # returned from PID calculations
    #maximum and minimum constraints
    'minimum_drive_speed':50,
    'maximum_drive_speed':180,
    'minimum_turn_speed':50,
    'maximum_turn_speed':180,
    }
    return df

def update_df(df, window1, roll_trim_system, ahrs_instrument, pitch_trim_system, pressuresensor):
    df['loop_count'] = df['loop_count'] + 1
    df['loop_speed'] = round(time.perf_counter() - df['SBC_powered_up_time'],3)
    df['current_time'] = '{:%H-%M-%S}'.format(datetime.datetime.now())
    df['SBC_powered_up_time'] = round(time.perf_counter(),3)

    df['pressure_mbar'] = 0 # read pressure sensor
    df['altitude_MSL'] = 0 # read pressure sensor
    df['altitude_local_pressure'] = 0 # read pressure sensor
    df['pressure_sensor_temperature_c'] = 0# read pressure sensor
    df['roll_AHRS_deg'] = 0 # read AHRS
    df['pitch_AHRS_deg'] = 0 # read AHRS
    df['heading_AHRS_deg'] = 0 # read AHRS
    df['roll_rate_AHRS_deg'] = 0 # read AHRS
    df['pitch_rate_AHRS_deg'] = 0 # read AHRS
    df['heading_rate_AHRS_deg'] = 0 # read AHRS

    df['heading_controller_enable'] = window1.heading_controller_enable_intvar.get()
    #df['drive_enable']
    #df['turn_enable']
    #df['csv_logging_enable']
    df['gui_enabled'] = window1.gui_enabled_intvar.get()
    #df['mission_script_enabled']

    if df['gui_enabled'] == 1:
        df['heading_setpoint'] = window1.heading_intvar.get()
        df['drive_speed'] = window1.drive_speed_intvar.get()
        df['turn_speed'] = window1.turn_speed_intvar.get()
    else:
        df['heading_setpoint'] = df['heading_setpoint']
        df['drive_speed'] = df['drive_speed']
        df['turn_speed'] = df['turn_speed']
    return df

def create_main_csv(df):
    if df['csv_logging_enable'] == 1:
        filetimestamp = "{:%H-%M-%S_%Y-%m-%d}".format(datetime.datetime.now())
        csvfilename = "./loggedData/" + filetimestamp + "_detectorover.csv"
        f = open(csvfilename, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(list(df.keys()))
        f.close()
        return csvfilename

def write_new_csv_row(df, csvfilename):
    if df['csv_logging_enable'] == 1:
        with open(csvfilename, mode='a', newline='') as f:
            csv.writer(f, delimiter=',').writerow(list(df.values()))
            f.close()
    return