import serial

# register addresses
GET_FW_REVISION       = 0xAA # (170)
FLASH_COMMIT          = 0xAB # (171)
RESET_TO_FACTORY      = 0xAC # (172)
ZERO_GYROS            = 0xAD # (173)
SET_HOME_POSITION     = 0xAE # (174)
SET_MAG_REFERENCE     = 0xB0 # (176)
RESET_EKF             = 0xB3 # (179)

DREG_HEALTH           = 0x55
DREG_GYRO_RAW_XY      = 0x56
DREG_GYRO_PROC_X      = 0x61
DREG_ACCEL_PROC_X     = 0x65
DREG_QUAT_AB          = 0x6D
DREG_EULER_PHI_THETA  = 0x70
DREG_GYRO_BIAS_X      = 0x89

CREG_COM_SETTINGS     = 0x00
CREG_COM_RATES1       = 0x01
CREG_COM_RATES2       = 0x02
CREG_COM_RATES3       = 0x03
CREG_COM_RATES4       = 0x04
CREG_COM_RATES5       = 0x05
CREG_COM_RATES6       = 0x06
CREG_COM_RATES7       = 0x07
CREG_GYRO_TRIM_X      = 0x0C
CREG_MAG_CAL1_1       = 0x0F
CREG_MAG_BIAS_X       = 0x18
CREG_ACCEL_CAL1_1     = 0x1B
CREG_ACCEL_BIAS_X     = 0x24

CREG_MISC_SETTINGS    = 0x08
CREG_MISC_SETTINGS_MAG= 0x01
CREG_MISC_SETTINGS_Q  = 0x02
CREG_MISC_SETTINGS_ZG = 0x04
CREG_MISC_SETTINGS_PPS= 0x100

REG_HIDDEN            = 0xF000
H_CREG_GYRO_VARIANCE  = REG_HIDDEN | 0x00
H_CREG_ACCEL_VARIANCE = REG_HIDDEN | 0x01
H_CREG_MAG_VARIANCE   = REG_HIDDEN | 0x02
H_CREG_ACCEL_TAU      = REG_HIDDEN | 0x11
H_CREG_GYRO_TAU       = REG_HIDDEN | 0x12
H_CREG_MAG_TAU        = REG_HIDDEN | 0x13
H_CREG_GYRO_ALIGN1_1  = REG_HIDDEN | 0x31
H_CREG_ACCEL_ALIGN1_1 = REG_HIDDEN | 0x52
H_CREG_MAG_ALIGN1_1   = REG_HIDDEN | 0x73
H_CREG_MAG_REF        = REG_HIDDEN | 0x7C

HEALTH_GPS   = 0x1
HEALTH_MAG   = 0x2
HEALTH_GYRO  = 0x4
HEALTH_ACCEL = 0x8
HEALTH_ACC_N = 0x10
HEALTH_MG_N  = 0x20
HEALTH_RES6  = 0x40
HEALTH_RES7  = 0x80
HEALTH_OVF   = 0x100

class UM7(object):
    """ um7 device object creation class """
    def __init__(self, serial_port='/dev/ttyS0', baudrate=115200):
        self.ser = serial.Serial(serial_port, baudrate, timeout=0.02)
        print("um7 serial device: " + str(self.ser.name))
        
        self.some_object_variable = 18
        pass

    def checksumcheck(self,  s):
        x = (s[-2:-1][0]<<8)|s[-1:][0]
        x = x if x < 0x8000 else x - 0xffff
        y = sum(s[0:-2])
        return ((0, 1)[x == y])

    def checksum_byte(self):
        #this will be a way to quickly split the last 2 bytes on a serial msg
        return

    def zeroGYRO(self): # send command to 0xB3 (179) to reset the  
        s = 0
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        msglist = [115, 110, 112, 0, 173, 1, 254] #creates a message to um7 sending RESET_EKF command
        # 115=s, 110=n, 112=p, PTbyte=0 for command, 179(0xB3) RESET_EKF address, (2<<8)|4 = checksum(516, 0x204)
        self.ser.write(msglist)
        s = list(bytearray(self.ser.read(15))) # recieves (max 16bytes)
        if self.checksumcheck(s) == 1:
            cmdoutcome = [s[0], s[1], s[2], s[3], s[4], s[5], s[6]]
        #    print(*cmdoutcome, sep=', ')
            return (("ZERO_GYRO failed", "ZERO_GYRO success")[cmdoutcome[3] == 0])
        else:
            print("checksum error")
            return "checksum error"

    def resetEKF(self): # send command to 0xB3 (179) to reset the  
        s = 0
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        msglist = [115, 110, 112, 0, 179, 2, 4] #creates a message to um7 sending RESET_EKF command
        # 115=s, 110=n, 112=p, PTbyte=0 for command, 179(0xB3) RESET_EKF address, (2<<8)|4 = checksum(516, 0x204)
        self.ser.write(msglist)
        s = list(bytearray(self.ser.read(15))) # recieves (max 16bytes)
        if self.checksumcheck(s) == 1:
            cmdoutcome = [s[0], s[1], s[2], s[3], s[4], s[5], s[6]]
        #    print(*cmdoutcome, sep=', ')
            return (("RESET_EKF failed", "RESET_EKF success")[cmdoutcome[3] == 0])
        else:
            print("checksum error")
            return "checksum error"

    def set_magnetic_reference(self): # send command to 0xB3 (179) to reset the  
        s = 0
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        msglist = [115, 110, 112, 0, 176, 2, 1] #creates a message to um7 sending RESET_EKF command
        # 115=s, 110=n, 112=p, PTbyte=0 for command, 179(0xB3) RESET_EKF address, (2<<8)| = checksum(516, 0x204)
        self.ser.write(msglist)
        s = list(bytearray(self.ser.read(15))) # recieves (max 16bytes)
        if self.checksumcheck(s) == 1:
            cmdoutcome = [s[0], s[1], s[2], s[3], s[4], s[5], s[6]]
        #    print(*cmdoutcome, sep=', ')
            return (("set_magnetic_reference failed", "set_magnetic_reference success")[cmdoutcome[3] == 0])
        else:
            print("checksum error")
            return "checksum error"

    def rollpitchyaw(self):
        s = 0
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        msglist = [115, 110, 112, 72, 112, 2, 9] # creates a message for um7 requesting data
        # 115 = s, 110 = n, 112=p, PTbyte 72=01001000, 112=(0x70) data register, (2<<8)|9=checksum 
        
        self.ser.write(msglist) #writes msg to um7 via serial

        s = list(bytearray(self.ser.read(15))) #recieve 15 bytes from um7 converts to bytearray then a list
    #   print(*s, sep=', ')

        checksumerror = self.checksumcheck(s)
    #   print("checksum error is: " + str(checksumerror))

        if checksumerror == 1:
            self.ser.reset_output_buffer() #clears buffers, this is probably optional
            self.ser.reset_input_buffer() #clears buffers, this is probably optional

            # phithetapsi = [roll, pitch, yaw]
            tmp = (s[5] << 8)| s[6] #roll data is in list [5] and [6]
            roll = tmp if tmp < 0x8000 else tmp - 0xffff
            phithetapsi = [(roll / 91.02222)]
        #    print(str(roll))

            tmp = (s[7] << 8)| s[8] #pitch data is in list [7] and [8]
            pitch = tmp if tmp < 0x8000 else tmp - 0xffff
            phithetapsi.append((pitch / 91.02222))
        #    print(str(pitch))

            tmp = (s[9] << 8)| s[10] # yaw data is in list [9] and [10]
            yaw = tmp if tmp < 0x8000 else tmp - 0xffff
            phithetapsi.append((yaw / 91.02222))
        #    print(str(yaw))
        else:
            print("checksum error")
            phithetapsi = [0, 0, 0]
        return phithetapsi

    def rollpitchyaw_rate(self):
            s = 0
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            msglist = [115, 110, 112, 72, 114, 2, 11] # creates a message for um7 requesting data
            # 115 = s, 110 = n, 112=p, PTbyte 72=01001000, 114=(0x72) data register, (2<<8)|11=checksum 
            # sum([115,110,112,72,114]) = checksum = [2, 11] or (2<<8)|11
            self.ser.write(msglist) #writes msg to um7 via serial

            s = list(bytearray(self.ser.read(15))) #recieve 15 bytes from um7 converts to bytearray then a list
        #   print(*s, sep=', ')

            checksumerror = self.checksumcheck(s)
        #   print("checksum error is: " + str(checksumerror))

            if checksumerror == 1:
                self.ser.reset_output_buffer() #clears buffers, this is probably optional
                self.ser.reset_input_buffer() #clears buffers, this is probably optional

                # phithetapsi = [roll, pitch, yaw]
                tmp = (s[5] << 8)| s[6] #roll data is in list [5] and [6]
                roll_rate = tmp if tmp < 0x8000 else tmp - 0xffff
                phithetapsi_rate = [(roll_rate / 16)]
            #    print(str(roll))

                tmp = (s[7] << 8)| s[8] #pitch data is in list [7] and [8]
                pitch_rate = tmp if tmp < 0x8000 else tmp - 0xffff
                phithetapsi_rate.append((pitch_rate / 16))
            #    print(str(pitch))

                tmp = (s[9] << 8)| s[10] # yaw data is in list [9] and [10]
                yaw_rate = tmp if tmp < 0x8000 else tmp - 0xffff
                phithetapsi_rate.append((yaw_rate / 16))
            #    print(str(yaw))
            else:
                print("checksum error")
                phithetapsi_rate = [0, 0, 0]
            return phithetapsi_rate

    def dreghealth(self):
        s = 0
        msglist = [115, 110, 112, 72, 85, 1, 238]
        # 115 = s, 110 = n, 112 = p, 72 = 01001000, 85 = 0x55 data register, (1 << 8)| 238 = checksum 
        self.ser.write(msglist)
        s = list(bytearray(self.ser.read(15)))
        print(str(s))

        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

        # healthbitslist = [b3 = s[5], b2 = s[6], b1 = s[7], b0 = s[8]]
        healthbitslist = [s[5], s[6], s[7], s[8]]
        return healthbitslist

    #while 1:
    #    phithetapsi = rollpitchyaw() 
    #   healthbitslist = dreghealth() 
    #   print("roll " + str(phithetapsi[0]) + " pitch " + str(phithetapsi[1]) + " yaw " + str(phithetapsi[2]))
    #   print("B3:" + str(healthbitslist[0]) + " B2:" + str(healthbitslist[1]) + " B1:" + str(healthbitslist[2]) + " B0 " + str(healthbitslist[3]))



