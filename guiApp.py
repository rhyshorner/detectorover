import tkinter
from tkinter import *
from tkinter import ttk
import time

class Application(tkinter.Frame):
    def __init__(self, df, master=None):
        super().__init__(master)
        self.master = master
        master.title('Detectorover GUI')
        master.geometry('%dx%d+%d+%d' % (530, 400, 20, 50))

        self.font_type = 'Helvetica'
        self.font_size = 12
        # added a delay between label updates to improve loop sleep performance
        self.label_update_countdown_timer = time.time()
        self.label_update_timer = 0.4

        window1_root_tab = ttk.Notebook(master)
        #overview_tab = ttk.Frame(window1_root_tab)
        pitch_trim_tab = ttk.Frame(window1_root_tab)
        roll_trim_tab = ttk.Frame(window1_root_tab)
        heading_ctrl_tab = ttk.Frame(window1_root_tab)
        AHRS_tab = ttk.Frame(window1_root_tab)
        pressure_tab = ttk.Frame(window1_root_tab)
        enabled_tab = ttk.Frame(window1_root_tab)
        
        #window1_root_tab.add(overview_tab, text="  overview  ")
        window1_root_tab.add(drive_system_tab, text="  pitch trim  ")
        window1_root_tab.add(AHRS_tab, text="  AHRS  ")
        window1_root_tab.add(pressure_tab, text="  pressure  ")
        window1_root_tab.add(enabled_tab, text="  enabled?  ")
        window1_root_tab.pack(expand=1, fill='both')
        self.pack()
        time.sleep(0.2)
        # scale and gui intput variables
        self.pitch_trim_intvar = IntVar()
        self.roll_trim_intvar = IntVar()
        self.heading_intvar = IntVar()

        self.gui_enabled_intvar = IntVar()
        self.gui_enabled_intvar.set(df['gui_enabled'])

#--------------------INPUTS------------------------------------
        # drive inputs
        self.drive_speed_setpoint = tkinter.Scale(drive_system_tab, font=(self.font_type,self.font_size), from_=-20, to=20, variable=self.pitch_trim_intvar, orient=HORIZONTAL, label="Pitch angle setpoint",length=500, width=15)
        self.drive_speed_setpoint.grid(row=4,column=4)
        self.drive_speed_setpoint.set(0)

        # pitch tab GUI label displays
        self.current_drive_speed_label = Label(drive_system_tab, font=(self.font_type,self.font_size))
        self.current_drive_speed_label.grid(row=5,column=4)

    def update_GUI_labels(self, df):
        self.master.update()
        if (time.time() - self.label_update_countdown_timer) > self.label_update_timer:
            self.current_drive_speed_label.config(text="Current Position: " + str(df['pitch_trim_current_position']))
            self.drive_speed_setpoint.config(text="Pitch angle setpoint: " + str(df['pitch_trim_setpoint']))
 
            self.label_update_countdown_timer = time.time()