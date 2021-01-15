# detectorover
a semi autonomous small scale car 

# task list

-   everything still
#----------------------------------------------------------------------------------------

## hardware;
-   1x Raspberrypi 3 model B V1.2
-   1x Adafruit 16-Channel PWM / Servo HAT for Raspberry Pi SKU: ADA2327
-   1x U-Blox NEO-6M GPS Module SKU:CEO5949
-   1x GPIO Stacking Header Extra-long 2x20 Pins

## hardware no longer used;
-   20A ESC brushed bidirectional SKU:DRI0047

# requirements
sudo apt-get install python-smbus
sudo apt-get install i2c-tools

# useful information and commands
## sudo i2cdetect -y 1
## rpi GPIO
-   persmission
$ sudo usermod -a -G gpio <username>
-   library used: RPi.GPIO
-   docs at: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
- GPIO.setmode(BOARD) to use GPIO pins as written on pcb, NOT the actual IC pin numbers