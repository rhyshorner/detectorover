import um7
try:
	um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200)
	#print("Zero rate gyro command has been sent.")
	um7.zeroGYRO()
except:
	print("um7 initialize failed.")
	print("Zero rate gyro command not sent")