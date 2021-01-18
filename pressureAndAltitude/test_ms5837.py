import ms5837

#begin i2c connection from ms5837 to rpi
sensor = ms5837.MS5837_30BA(1) # Default I2C bus is 1 (Raspberry Pi 3)
localbarometricpressure = 102200 #current local barometric pressure at surface

# initialise pressure sensor 
sensor.init()
sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
#sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
sensor.read()
print("ms5837 initlize success.")

#------------- Pressure sensor - read values ------------------------
while True:
    sensor.read()
    mbar = round(sensor.pressure(), 2) # Default is mbar (no arguments)
    celciustemp = round(sensor.temperature(), 2) # Default is degrees C (no arguments)
    farentemp = round(sensor.temperature(ms5837.UNITS_Farenheit), 1)
    vesseldepth = round(sensor.depth(localbarometricpressure), 3)
    print("mbar: " + str(mbar))
    print("celciustemp: " + str(celciustemp))
    print("vesseldepth: " + str(vesseldepth))
    
