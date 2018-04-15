#1 Start Stopped
#2 Apply Torque Drag
#3 Determine Accel
#4 Speed
#5 Distance
#6 Delta Time
#7 Repeat Steps 2 - 6 Until Time Reached


import csv
import math
from arrays import *


# Constants
dLim = 2
spRatio = 85 / 12
kMass = 120
wheelDia = .5588
outputTorque = 6.9
dragCoefficent = .3
frontal = .56
airDensity = 1.225
forceTotal = 10
clutchSlip = 1.0
drivenWheelCir = math.pi * wheelDia


"""
    Method to simulate a Go-Kart run
    
    until:    time to go until
    step:     time step (increment)
    throttle: throttle percentage divisible by 10
"""
def simulate_run(until:int, step:float, throttle:int)->bool:
        
    try:
        fname = "run_" + str('%.3f' % step).split('.')[1] + "ms.txt"
        
        #Starting Values
        drag = 0
        output = []
        dist = 0
        velSprint = 0
        distSprint = 0	
        clutchSprint = 0
        rpm = 2000
        timeSum = 0
        lockup = False

        # Main Loop
        for x in range(0, (int)(until * (1 / step) + 1)):
            
            # Calculated
            kAccel = (((outputTorque * spRatio * 2) / wheelDia) - forceTotal - drag) / kMass # mph
            velSpeed = velSprint + kAccel * step # meters / second
            dist += velSpeed * step # meters
            drag = (velSpeed ** 2) * airDensity * dragCoefficent * frontal / 2 # Drag Coefficient
            clutchSpeed = velSpeed * 60 * spRatio / drivenWheelCir 
            slip = (rpm - clutchSprint) / rpm
		    
		    # for slip < 0 we need to look up engine speeed using the clutchSpeed. Look up outputTorque == engine torque.   
		    # if lockup == true or
		    # look up the table.
            if (lockup == True or slip <= 0):
                lockup = True
                
                rpm = clutchSpeed
                
                # Lookup torque value
                torque = getTorque(rpm, throttle)
           
            # Output
            output.append([round(timeSum, dLim), round(kAccel, dLim), round(velSpeed, dLim), round(dist, dLim), round(slip, dLim)])
            
            # Iterate Variables
            velSprint = velSpeed
            distSprint = dist

            clutchSprint = clutchSpeed
            timeSum += step
		    
        # Finally
        with open('runs/' + fname, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["Time Step", "Kart Accel", "Vehicle Speed", "Total Distance", "Clutch Slip"])
            for iteration in output:
                filewriter.writerow(iteration)
        return True
    except:
        return False


"""
    Method to get torque
    
    rpm:      between 1400 and 3600
    throttle: percentage divisible by 10
"""
def getTorque(rpm:int, throttle:int)->float:

    # Ensure RPM is between 1400 and 3600
    if (rpm >= 1400 and rpm <= 3600):
        
        # Parse RPM as a string and strip decimal values
        rString = str(int(rpm))
        try:
            # Only executes if no errors finding the "00" in rString
            test = (rString.index("00") != 2)
            
            # Gets torque at rpm if rpm is divisible by 100
            return findTorque(rpm / 100, throttle)
            
        except:
            # The first two digits of RPM (used for torque lookup)
            gets = int(rString[0:2])
            
            # The last two digits of RPM (used for weighting torque multiplcation)
            remain = int(rString[2:4])

            # Find and weight the two torque values
            t1 = findTorque(gets, throttle) * (float(100 - remain) / 100)
            t2 = findTorque(gets + 1, throttle) * (float(remain) / 100)
            
            # Return the sum of weighted torques
            return t1 + t2


"""
    Lookup method to find torques in arrays.py
    
    msbRPM:   two-digit rpm (rpm / 100)
    thorttle: throttle percentage divisble by 10
"""
def findTorque(msbRPM:int, throttle:int)->float:
    # msbRPM = rpm / 100
    
    # Get Throttle Row based on RPM
    index = msbRPM - 14
    
    # Define array name to retrieve torque from based on throttle
    arrayName = "t" + str(throttle) + "throttleArray"
    
    # Get torque at certain throttle and RPM
    cmd = str(arrayName + "[" + str(index) + "][0]")
    torque = eval(cmd)
    return torque


"""
    Simulate Go-Kart Runs
    Generate CSV Files in runs folder
"""
print(simulate_run(100, .5, 100))
print(simulate_run(100, .25, 100))
print(simulate_run(100, .05, 100))


"""
    Testing for getTorque() and findTorque() functions
    (No longer needed)
"""
# print("1400rpm @ 100% throttle")
# print("finalTorque: " + str(getTorque(1400, 100)))
# print("\n1475rpm @ 100% throttle")
# print("finalTorque: " + str(getTorque(1475, 100)))
