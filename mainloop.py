from pressureAndAltitude import pressureSensor
from attitudeAndHeading import ahrs
from driveAndSteering import drivesystem
from missionPlanner import mission_planner
from headingController import heading_controller

import datetime, time, sys, csv
from guiApp import *
from dataFrame_and_csv import *

# create local dataframe called df{}
df = create_dataframe() #from dataFrame_and_csv.py

# Setup class objects, initialize sensors and control systems
pressuresensor = pressureSensor.PressureSensor(local_pressure=101325)

ahrs_instrument = ahrs.Um7Ahrs()

drive_system = driveSystem.DriveSystem(min_power=50,
                                        max_power=180,
                                        proportional_gain=df['roll_trim_P_gain'],
                                        intergral_gain=df['roll_trim_I_gain'],
                                        derivative_gain=df['roll_trim_D_gain'],
                                        )

mission_script = mission_planner.MissionPlanner(df['mission_script_type'])

heading_control = heading_controller.HeadingController(df['heading_ctrl_P_gain'],
                                                    df['heading_ctrl_I_gain'],
                                                    df['heading_ctrl_D_gain'],
                                                    df['maximum_roll'],
                                                    )

# Create gui app here and begin with mainloop()
window1 = tkinter.Tk()
window1 = Application(df, master=window1)

# create csv and add row function
csvfilename = create_main_csv(df) #from dataFrame_and_csv.py
# create csv for live graph to feed from
graph_csvfilename = create_new_graph_csv_row(df)

# Run main loop here
#try:
while True:
    #---------collect and update sensor readings----------------
    df = update_df(df, window1, drive_system, ahrs_instrument, pressuresensor)

    #---------set or check mission script-----------------------
    if df['gui_enabled'] == 0: # this is an interlock between mission script and gui input
        df['pitch_trim_setpoint'], df['roll_trim_setpoint'], df['heading_setpoint'] = mission_script.mission_script_event_check(df['mission_script_enabled'], df['depth_m_MSL'], df['pitch_trim_setpoint'], df['roll_trim_setpoint'], df['heading_setpoint'])

    #---------control loop section------------------------------
    df['heading_ctrl_error'], df['roll_trim_setpoint'], df['heading_ctrl_Pterm'], df['heading_ctrl_Iterm'], df['heading_ctrl_Dterm'] = heading_control.control_loop(df['heading_controller_enable'], df['heading_setpoint'], df['heading_AHRS_deg'], df['roll_trim_setpoint'])
    df['roll_trim_error'], df['roll_trim_output'], df['roll_trim_velocity'], df['roll_trim_Pterm'], df['roll_trim_Iterm'], df['roll_trim_Dterm'] = roll_trim_system.control_loop(df['roll_trim_enable'], df['roll_trim_setpoint'], df['roll_AHRS_deg'])
    df['pitch_trim_error'], df['pitch_trim_output'], df['pitch_trim_velocity'], df['pitch_trim_Pterm'], df['pitch_trim_Iterm'], df['pitch_trim_Dterm'] = pitch_trim_system.control_loop(df['pitch_trim_enable'], df['pitch_trim_setpoint'], df['pitch_AHRS_deg'])

    #----------update csv---------------------------------------
    write_new_csv_row(df, csvfilename) #from dataFrame_and_csv.py
    write_new_graph_csv_row(df, graph_csvfilename) #from dataFrame_and_csv.py

    #update tkinter gui window
    window1.update_GUI_labels(df) # from guiApp.py

# except:
#     print("script terminated.")
#     roll_trim_system.tict500.set_target_velocity(0)
#     pitch_trim_system.tict500.set_target_velocity(0)
