#1 Start Stopped
#2 Apply Torque Drag
#3 Determine Accel
#4 Speed
#5 Distance
#6 Delta Time
#7 Repeat Steps 2 - 6 Until Time Reached

import csv
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
drivenWheelCir = 1.76

def simulate_run(until, step, throttle):
    
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
		
        # Output
        output.append([round(timeSum, dLim), round(kAccel, dLim), round(velSpeed, dLim), round(dist, dLim), round(slip, dLim)])
        
        # Iterate Variables
        velSprint = velSpeed
        distSprint = dist
        clutchSprint = clutchSpeed
        timeSum += step
		
		# for slip < 0 we need to look up engine speeed using the clutchSpeed. Look up outputTorque == engine torque.   
		# if lockup == true or
		# look up the table.
        if (lockup == True or slip <= 0):
            lockup = True
            
            rpm = clutchSpeed
		
    # Finally
    with open('runs/' + fname, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Time Step", "Kart Accel", "Vehicle Speed", "Total Distance", "Clutch Slip"])
        for iteration in output:
            filewriter.writerow(iteration)
            
simulate_run(100, .5, 1)
simulate_run(100, .25, 1)
simulate_run(100, .05, 1)
