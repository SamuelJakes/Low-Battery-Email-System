#!/usr/bin/python3
import time
import sys
from ads1015 import ADS1015

# Time between each voltage read in seconds
# THIS SHOULD BE SET TO 30 OR SO BEFORE RUNNING
readDelay = 10

# Define points on characteristic curve for a particular battery
# The points are: [voltage, battery percent full]
# This is assumed to be in descending order on a monotonically decreasing graph
powertechLithium12point8V = [[13.65, 100], [13.38, 98.96], [13.06, 96.88], [12.92, 58.33], [12.68, 21.88], [12.43, 10.13], [11.33, 4.17], [10.15, 1.08], [0, 0]]

# A function for interpolating between points picked on a monotonically decreasing graph
def linearInterpolate(points, value):

    # Check that the points are monotonically decreasing
    check = True
    for i in range(len(points)):
        if i+1 >= len(points):
            break
        check = check and points[i][0] >= points[i+1][0]
        check = check and points[i][1] >= points[i+1][1]

    if not check:
        sys.exit("Error, the given points for battery interpolation are not monotonically decreasing")



    # If the measured value is outside of the point ranges, then return the point at the extremity
    if value >= points[0][0]:
        return round(points[0][1])
    if value <= points[-1][0]:
        return round(points[-1][1])

    # Otherwise return a value linearly interpolated between 2 points

    for i in range(len(points)):

        # if the value is between this point and the next point then interpolate
        if value <= points[i][0] and value >= points[i+1][0]:
            fraction=(points[i][0] - value)/(points[i][0] - points[i+1][0])
            return round(points[i][1] - fraction*(points[i][1] - points[i+1][1]))

    # If nothing is returned by this point then something went wrong
    sys.exit("Error, the given points for battery interpolation are not monotonically decreasing")
    return -1

# Measure voltages
ads1015 = ADS1015()
ads1015.set_mode('single')
ads1015.set_programmable_gain(2.048)
ads1015.set_sample_rate(1600)
batteryFile = open('batteryLevel.txt', 'w')
try:
    while True:
        value = ads1015.get_voltage(channel='in0/gnd')
        # value = input("enter voltage value: ")
        batteryLevel = linearInterpolate(powertechLithium12point8V, float(value))
        print("Detected battery level: " + str(batteryLevel))
        batteryFile.write(str(batteryLevel) + "\n")
        batteryFile.flush()
        time.sleep(readDelay)
except KeyboardInterrupt:
    batteryFile.close()



