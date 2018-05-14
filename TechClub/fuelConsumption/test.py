#1 Start Stopped
#2 Apply Torque Drag
#3 Determine Accel
#4 Speed
#5 Distance
#6 Delta Time
#7 Repeat Steps 2 - 6 Until Time Reached


import csv
import math
import sys
from arrays import *

class SimulateRun:
    
    def __init__(self):
        """
            Contructor Function
            
            Defines all constants
            (Will add arguments later)
        """

        # Constants
        self._dLim = 2
        self._spRatio = 85 / 12
        self._kMass = 120
        self._wheelDia = .5588
        self._outputTorque = 6.9
        self._dragCoefficent = .3
        self._frontal = .56
        self._airDensity = 1.225
        self._forceTotal = 10
        self._clutchSlip = 1.0
        self._drivenWheelCir = math.pi * self._wheelDia

    @classmethod
    def simulate_run(self, until:int, step:float, throttle:int)->bool:
        """
            Method to simulate a Go-Kart run

            until:    time to go until
            step:     time step (increment)
            throttle: throttle percentage divisible by 10
        """

        if (type(until) != int or type(step) != float or type(throttle) != int):
            raise TypeError('parameters must be integer, float, integer!')
        else:
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


            # Main Loop
            for x in range(0, (int)(until * (1 / step) + 1)):

                # Calculated
                kAccel = (((self._outputTorque * self._spRatio * 2) / self._wheelDia) - self._forceTotal - drag) / self._kMass # mph
                velSpeed = velSprint + kAccel * step # meters / second
                dist += velSpeed * step # meters
                drag = (velSpeed ** 2) * self._airDensity * self._dragCoefficent * self._frontal / 2 # Drag Coefficient
                clutchSpeed = velSpeed * 60 * self._spRatio / self._drivenWheelCir 
                slip = (rpm - clutchSprint) / rpm

                # for slip < 0 we need to look up engine speeed using the clutchSpeed. Look up outputTorque == engine torque.   
                # if lockup == true or
                # look up the table.
                if (lockup == True or slip <= 0):
                    lockup = True

                    rpm = clutchSpeed

                    # Lookup torque value
                    torque = self._calcTorque(int(rpm), throttle)
                    # print([int(rpm), throttle])
                    # print(self._calcTorque(int(rpm), throttle))
                    # print("sys torque: " + str(torque))


                # Output
                output.append([round(timeSum, self._dLim), round(kAccel, self._dLim), round(velSpeed, self._dLim), round(dist, self._dLim), round(slip, self._dLim)])

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

    @classmethod
    def _calcTorque(self, rpm:int, throttle:int)->float:
        """
            Method to calculate torque

            rpm:      between 1400 and 3600
            throttle: percentage divisible by 10
        """

        if ((type(rpm) != int) or (type(throttle) != int)):
            raise TypeError('Both parameters must be integers!')
        else:
            # Ensure RPM is between 1400 and 3600
            if (rpm >= 1400 and rpm <= 3600):

                # Parse RPM as a string and strip decimal values
                rString = str(int(rpm))
                try:
                    # Only executes if no errors finding the "00" in rString
                    test = (rString.index("00") != 2)

                    # Gets torque at rpm if rpm is divisible by 100
                    finTorque = self._findTorque(int(rpm / 100), throttle)

                except:
                    # The first two digits of RPM (used for torque lookup)
                    gets = int(rString[0:2])

                    # The last two digits of RPM (used for weighting torque multiplcation)
                    remain = int(rString[2:4])

                    # Find and weight the two torque values
                    t1 = self._findTorque(gets, throttle) * (float(100 - remain) / 100)
                    t2 = self._findTorque(gets + 1, throttle) * (float(remain) / 100)

                    # Return the sum of weighted torques
                    finTorque = t1 + t2
                return finTorque

    @classmethod
    def _findTorque(self, msbRPM:int, throttle:int)->float:
        """
            Lookup method to find torques in arrays.py

            msbRPM:   two-digit rpm (rpm / 100)
            thorttle: throttle percentage divisble by 10
        """
        if (type(msbRPM) != int or type(throttle) != int):
            raise TypeError('Both parameters must be integers!')
        else:
            return self.__findTuple(msbRPM, throttle)[0]

    @classmethod
    def _findPower(self, msbRPM:int, throttle:int)->float:
        """
            Lookup method to find powers in arrays.py

            msbRPM:   two-digit rpm (rpm / 100)
            thorttle: throttle percentage divisble by 10
        """
        if (type(msbRPM) != int or type(throttle) != int):
            raise TypeError('Both parameters must be integers!')
        else:
            return self.__findTuple(msbRPM, throttle)[1]

    @classmethod
    def _findBSFC(self, msbRPM:int, throttle:int)->float:
        """
            Lookup method to find BSFC's in arrays.py

            msbRPM:   two-digit rpm (rpm / 100)
            thorttle: throttle percentage divisble by 10
        """
        if (type(msbRPM) != int or type(throttle) != int):
            raise TypeError('Both parameters must be integers!')
        else:
            return self.__findTuple(msbRPM, throttle)[3]

    @classmethod
    def __findTuple(self, msbRPM:int, throttle:int)->tuple:
        """
            Lookup method to find tuples in arrays.py

            msbRPM:   two-digit rpm (rpm / 100)
            thorttle: throttle percentage divisble by 10
        """

        # msbRPM = rpm / 100
        if (type(msbRPM) != int or type(throttle) != int):
            raise TypeError('Both parameters must be integers!')
        else:
            # Validate RPM Value
            if (msbRPM >= 14 and msbRPM <= 36):
                # Get Throttle Row based on RPM
                index = int(msbRPM - 14)

                # Validate Throttle Value to reduce chance of error
                if ((throttle % 10 == 0) and (throttle > 0 and throttle <= 100)):
                    # Define array name to retrieve tuple from based on throttle
                    arrayName = str("t" + str(int(throttle)) + "throttleArray")

                    # Get tuple at certain throttle and RPM
                    cmd = str(arrayName + "[" + str(index) + "]")
                    myTuple = eval(cmd)
                    return myTuple


# Simulate Go-Kart Run
# Generate CSV Files in runs folder
s = SimulateRun()
print(s.simulate_run(100, .5, 100))
print(s.simulate_run(100, .25, 100))
print(s.simulate_run(100, .05, 100))


# Testing for getTorque() and findTorque() functions
# (No longer needed)

# print("1400rpm @ 100% throttle")
# print("finalTorque: " + str(s.getTorque(1400, 100)))
# print("\n1475rpm @ 100% throttle")
# print("finalTorque: " + str(s.getTorque(1475, 100)))