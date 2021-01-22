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
        drive_system_tab = ttk.Frame(window1_root_tab)
        AHRS_tab = ttk.Frame(window1_root_tab)
        
        #window1_root_tab.add(overview_tab, text="  overview  ")
        window1_root_tab.add(drive_system_tab, text="  pitch trim  ")
        window1_root_tab.add(AHRS_tab, text="  AHRS  ")
        window1_root_tab.pack(expand=1, fill='both')
        self.pack()
        # scale and gui intput variables
        self.drive_speed_entry_box_stringvar = StringVar()
        self.drive_speed_intvar = IntVar()
        self.turn_speed_entry_box_stringvar = StringVar()
        self.turn_speed_intvar = IntVar()
        self.heading_intvar = IntVar()

        self.heading_controller_enable_intvar = IntVar()
        self.heading_controller_enable_intvar.set(df['heading_controller_enable'])
        self.gui_enabled_intvar = IntVar()
        self.gui_enabled_intvar.set(df['gui_enabled'])

        def set_turn_speed():
            x = int(self.turn_speed_setpoint_entry.get())
            if x > 180:
                x = 180
            elif x < -180:
                x = -180
            self.turn_speed_intvar.set(x)
        def set_turn_stop():
            self.turn_speed_intvar.set(0)

        def set_drive_speed():
            x = int(self.drive_speed_setpoint_entry.get())
            if x > 180:
                x = 180
            elif x < -180:
                x = -180
                
            self.drive_speed_intvar.set(x)
        def set_drive_stop():
            self.drive_speed_intvar.set(0)
#--------------------INPUTS------------------------------------
        # drive_tab inputs
        # drive
        self.current_drive_speed_label = Label(drive_system_tab, font=(self.font_type,self.font_size))
        self.current_drive_speed_label.grid(row=0,column=0)
        self.drive_speed_setpoint_entry = tkinter.Entry(drive_system_tab)
        self.drive_speed_setpoint_entry.grid(row=0,column=1)
        self.drive_speed_button = Button(drive_system_tab, text="set speed", bg="green3", activebackground="green4",  command=set_drive_speed)
        self.drive_speed_button.grid(row=0, column=2)
        self.drive_stop_button = Button(drive_system_tab, text="STOP", bg="red", activebackground="red3", command=set_drive_stop)
        self.drive_stop_button.grid(row=0, column=3)

        # turn
        self.current_turn_speed_label = Label(drive_system_tab, font=(self.font_type,self.font_size))
        self.current_turn_speed_label.grid(row=1,column=0)
        self.turn_speed_setpoint_entry = tkinter.Entry(drive_system_tab)
        self.turn_speed_setpoint_entry.grid(row=1,column=1)
        self.turn_speed_button = Button(drive_system_tab, text="set speed", bg="green3", activebackground="green4",  command=set_turn_speed)
        self.turn_speed_button.grid(row=1, column=2)
        self.turn_stop_button = Button(drive_system_tab, text="STOP", bg="red", activebackground="red3", command=set_turn_stop)
        self.turn_stop_button.grid(row=1, column=3)

        # after combined
        self.LHS_motor_speed_setpoint_label = Label(drive_system_tab, font=(self.font_type,self.font_size))
        self.LHS_motor_speed_setpoint_label.grid(row=5,column=0)
        self.RHS_motor_speed_setpoint_label = Label(drive_system_tab, font=(self.font_type,self.font_size))
        self.RHS_motor_speed_setpoint_label.grid(row=6,column=0)


    def update_GUI_labels(self, df):
        self.master.update()
        # drive_tab inputs
        if (time.time() - self.label_update_countdown_timer) > self.label_update_timer:
            self.current_drive_speed_label.config(text="Current drive speed: " + str(df['drive_speed']))
            self.current_turn_speed_label.config(text="Current turn speed: " + str(df['turn_speed']))
            self.LHS_motor_speed_setpoint_label.config(text="LHS drive speed: " + str(df['LHS_motor_speed_setpoint']))
            self.RHS_motor_speed_setpoint_label .config(text="RHS drive speed: " + str(df['RHS_motor_speed_setpoint']))

            self.label_update_countdown_timer = time.time()