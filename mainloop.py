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

ahrs_instrument = ahrs.Mpu6050Ahrs()

drive_system = drivesystem.DriveSystem(min_drive_speed=df['minimum_drive_speed'],
                                        max_drive_speed=df['maximum_drive_speed'],
                                        min_turn_speed=df['minimum_turn_speed'],
                                        max_turn_speed=df['maximum_turn_speed'],
                                        )

mission_script = mission_planner.MissionPlanner(df['mission_script_type'])

heading_control = heading_controller.HeadingController(df['heading_ctrl_P_gain'],
                                                    df['heading_ctrl_I_gain'],
                                                    df['heading_ctrl_D_gain'],
                                                    df['maximum_turn_speed']
                                                    )

# Create gui app here and begin with mainloop()
window1 = tkinter.Tk()
window1 = Application(df, master=window1)

# create csv and add row function
csvfilename = create_main_csv(df) #from dataFrame_and_csv.py

# Run main loop here
#try:
while True:
    #---------collect and update sensor readings----------------
    df = update_df(df, window1, drive_system, ahrs_instrument, pressuresensor)

    #---------set or check mission script-----------------------
    if df['gui_enabled'] == 0: # this is an interlock between mission script and gui input
        mission_script.mission_script_event_check(df['mission_script_enabled'])

    #---------control loop section------------------------------
    df['heading_ctrl_error'], df['turn_speed'], df['heading_ctrl_Pterm'], df['heading_ctrl_Iterm'], df['heading_ctrl_Dterm'] = heading_control.control_loop(df['heading_controller_enable'], df['heading_setpoint'], df['heading_AHRS_deg'], df['turn_speed'])
    drive_system.drive(df['drive_enable'], df['drive_speed'], df['drive_time'])

    #----------update csv---------------------------------------
    write_new_csv_row(df, csvfilename) #from dataFrame_and_csv.py

    #update tkinter gui window
    window1.update_GUI_labels(df) # from guiApp.py

# except:
#     print("script terminated.")
#     roll_trim_system.tict500.set_target_velocity(0)
#     pitch_trim_system.tict500.set_target_velocity(0)
