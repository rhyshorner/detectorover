import um7
try:
	um7 = um7.UM7(serial_port='/dev/ttyS0', baudrate=115200)
	#print("Reset EKF command has been sent.")
	um7.resetEKF()
except:
	print("um7 initialize failed.")
	print("magnetic reference command not sent")