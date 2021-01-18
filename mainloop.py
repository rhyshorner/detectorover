from pressureAndAltitude import pressureSensor
from attitudeAndHeading import ahrs
from trimSystem import trimsystem
from missionPlanner import mission_planner
from headingController import heading_controller

import datetime, time, sys, csv
import RPi.GPIO as GPIO
from guiApp import *
from dataFrame_and_csv import *

#jobs to complete;
#-  GUI disabled functioned grayed out
#-  GUI enable/disable checkboxes on GUI

# create local dataframe called df{}
df = create_dataframe() #from dataFrame_and_csv.py

# Setup class objects, initialize sensors and control systems
pressuresensor = pressureSensor.PressureSensor(local_pressure=101325)

ahrs_instrument = ahrs.Um7Ahrs()

roll_trim_system = trimsystem.TrimSystem(14, 
                                        "roll", 
                                        max_motorsteps=2200,
                                        offset=0, 
                                        full_travel_mm=2200,
                                        proportional_gain=df['roll_trim_P_gain'],
                                        intergral_gain=df['roll_trim_I_gain'],
                                        derivative_gain=df['roll_trim_D_gain'],
                                        ) #0 is port, 2200 is strb

pitch_trim_system = trimsystem.TrimSystem(13, 
                                        "pitch", 
                                        max_motorsteps=4200, 
                                        offset=0, 
                                        full_travel_mm=4200,
                                        proportional_gain=df['pitch_trim_P_gain'],
                                        intergral_gain=df['pitch_trim_I_gain'],
                                        derivative_gain=df['pitch_trim_D_gain'],
                                        )#0 is rear, 4200 is fore

mission_script = mission_planner.MissionPlanner(df['mission_script_type'])

heading_control = heading_controller.HeadingController(df['heading_ctrl_P_gain'],
                                                    df['heading_ctrl_I_gain'],
                                                    df['heading_ctrl_D_gain'],
                                                    df['maximum_roll'],
                                                    )

GPIO.setmode(GPIO.BCM) # setting up the pin labels used (either bcm pins or board label)
GPIO.setup(17,GPIO.IN) # making gpio an input

# Create gui app here and begin with mainloop()
window1 = tkinter.Tk()
window1 = Application(df, master=window1)

# create csv and add row function
csvfilename = create_main_csv(df) #from dataFrame_and_csv.py
# create csv for live graph to feed from
graph_csvfilename = create_new_graph_csv_row(df)
    
# Setup physical motors and send them to pre-determined center of mass positions
#---initialize motors and send to home---
roll_trim_system.check_if_uncertain_and_send_home(df['roll_trim_enable'])
pitch_trim_system.check_if_uncertain_and_send_home(df['pitch_trim_enable'])
#---once trimsystem motor positions are 'certain' continue
roll_trim_system.wait_for_homing_to_complete(df['roll_trim_enable'])
pitch_trim_system.wait_for_homing_to_complete(df['pitch_trim_enable'])

# to begin begining of script
# print(" ")
# input("Press enter to begin script or GUI")
print("script running.")

# Run main loop here
#try:
while True:
    #---------collect and update sensor readings----------------
    df = update_df(df, window1, roll_trim_system, ahrs_instrument, pitch_trim_system, pressuresensor)

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
