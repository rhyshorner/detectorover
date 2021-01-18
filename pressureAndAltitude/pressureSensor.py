# class object for miniray which uses ms5837 module

from . import ms5837
import time

class PressureSensor(object):
    """ miniray's pressure sensor management class """
    def __init__(self, local_pressure=101325):
        self.pressure_sensor = ms5837.MS5837_30BA(1) # Default I2C bus is 1 (Raspberry Pi 3)
        self.initialise_pressure_sensor()
        self.local_pressure = local_pressure # should be in pascals eg(1013.25mb = 101325 Pascals)
        self.mean_sea_level_pressure = 101325
        self.self_timer = time.time()
        self.max_read_speed_timer = 0.4

        self.vertical_speed_countdown_timer = time.time()
        self.vertical_speed_read_timer = 0.3
        self.last_depth = self.depth_meters()	
        self.vertical_speed = 0

        pass

    def initialise_pressure_sensor(self):
        try:
            self.pressure_sensor.init()
            self.pressure_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
            #self.pressure_sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
            self.pressure_sensor.read()
            print("ms5837 initlize success.")
        except:
            print("ms5837 failed initialization!")
            print("trying again...")
            try:
                time.sleep(0.200)
                self.pressure_sensor.init()
                self.pressure_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
                #self.pressure_sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
                self.pressure_sensor.read()
                print("ms5837 initlize success.")
            except:
                print("ms5837 failed twice, giving up.")

    def pressure_mbar(self):
        if (time.time() - self.self_timer) > self.max_read_speed_timer:
            self.pressure_sensor.read()
            self.self_timer = time.time()
        return self.pressure_sensor.pressure()

    def vertical_speed_estimate(self):
        if (time.time() - self.vertical_speed_countdown_timer) > self.vertical_speed_read_timer:
            self.vertical_speed = round((self.depth_meters() - self.last_depth) / (time.time() - self.vertical_speed_countdown_timer), 3)
            self.last_depth = self.depth_meters()	
            self.vertical_speed_countdown_timer = time.time()
        return self.vertical_speed

    def depth_meters(self):
        #self.pressure_sensor.read()
        return self.pressure_sensor.depth(self.local_pressure)

    def depth_meters_MSL(self):
        #self.pressure_sensor.read()
        return self.pressure_sensor.depth(self.mean_sea_level_pressure)

    def sensor_temperature(self):
        #self.pressure_sensor.read()
        return self.pressure_sensor.temperature()

    def print_object_variable(self):
        print(self.some_object_variable)  
        return              

    



#sensor.read()
#mbar = round(sensor.pressure(), 2) # Default is mbar (no arguments)
#celciustemp = round(sensor.temperature(), 2) # Default is degrees C (no arguments)
#farentemp = round(sensor.temperature(ms5837.UNITS_Farenheit), 1)
#vesseldepth = round(sensor.depth(localbarometricpressure), 3)