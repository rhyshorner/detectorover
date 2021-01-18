import pandas as pd
import matplotlib.pyplot as plt
import time

plt.style.use('fivethirtyeight')

print("example... '16-04-37_2020-12-15_miniray.csv'")
csvfilename = input("What is the name of the csv file to graph? ")

data = pd.read_csv('../loggedData/' + str(csvfilename))
x = data['loop_count']
y1 = data['pitch_AHRS_deg']
y2 = data['pitch_trim_setpoint']
#y3 = data['pitch_trim_Dterm']

plt.cla()

plt.plot(x, y1, label='Channel 1')
plt.plot(x, y2, label='Channel 2')
#plt.plot(x, y3, label='Channel 3')

plt.legend(loc='upper left')
plt.tight_layout()
plt.show()