#1 Start Stopped
#2 Apply Torque Drag
#3 Determine Accel
#4 Speed
#5 Distance
#6 Delta Time
#7 Repeat Steps 2 - 6 Until Time Reached

import csv

# Constants
dLim = 2
spRatio = 85 / 12
kMass = 120
wheelDia = .5588
outputTorque = 6.9
rpm = 2000
forceTotal = 10
clutchSlip = 1.0

def simulate_run(until, step):
    
    fname = "run_" + str('%.3f' % step).split('.')[1] + "ms.txt"
    
    #Starting Values
    output = []
    dist = 0
    velSprint = 0
    distSprint = 0
    timeSum = 0

    # Main Loop
    for x in range(0, (int)(until * (1 / step) + 1)):
        
        # Calculated
        kAccel = (((outputTorque * spRatio * 2) / wheelDia) - forceTotal) / kMass # mph
        velSpeed = velSprint + kAccel * step # meters / second
        dist += velSpeed * step # meters
        
        # Output
        output.append([round(timeSum, dLim), round(kAccel, dLim), round(velSpeed, dLim), round(dist, dLim)])
        
        # Iterate Variables
        velSprint = velSpeed
        distSprint = dist
        timeSum += step
        
    # Finally
    with open('runs/' + fname, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Time Step", "Kart Accel", "Vehicle Speed", "Total Distance"])
        for iteration in output:
            filewriter.writerow(iteration)
            
simulate_run(20, .5)
simulate_run(20, .25)
simulate_run(20, .05)