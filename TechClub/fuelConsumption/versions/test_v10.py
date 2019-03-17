#1 Start Stopped
#2 Apply Torque Drag
#3 Determine Accel
#4 Speed
#5 Distance
#6 Delta Time
#7 Repeat Steps 2 - 6 Until Time Reached


import csv
import math
from components.mymath import calcTorque, calcBSFC, calcPower
from components.enginestate import EngineState

class SimulateRun:
    """
        Class used for modeling Go-Kart runs for WDHS Tech Club
        
        This class in used to run the simulate_run() subroutine
        and has the purpose of optimizing fuel efficiency on
        a real life go kart for WEEVA competitions for the Western
        Dubuque High School racing team.
    """
    
    def __init__(self, vars = {}):
        """
            Contructor Function
            
            Defines all constants.
            Takes a dictionary with the
            { dLim => decimal delimter,
            spRatio => sprocket ratio,
            kMass => kart mass,
            outputTorque => engine output torque (Nm),
            dragCoefficent => coefficient of drag,
            frontal => kart frontal area (m^2),
            airDensity => density of air,
            forceTotal => total of forces acting on kart,
            clutchSlip => slip to start at (decimal %),
            state => engine state (from EngineState enum) }
        """

        if (type(vars) != dict):
            vars = {}
        
        # Constants
        # Decimal Delimiter
        self._dLim = int(vars.get('dLim', 2))
        
        # Sprocket Ratio
        self._spRatio = float(vars.get('spRatio', 96 / 11))
        
        # Kart Mass
        self._kMass = float(vars.get('kMass', 122.472)) # With 170lb driver
        # self._kMass = float(vars.get('kMass', 48.9888)) # Kart Mass

        # Wheel Diameter
        self._wheelDia = float(vars.get('wheelDia', .4826))

        # Engine Output Torque (Nm)
        self._outputTorque = float(vars.get('outputTorque', 6.9))

        # Coefficient of Drag
        self._dragCoefficent = float(vars.get('dragCoefficent', .3))

        # Kart Frontal Area (m^2)
        self._frontal = float(vars.get('frontal', .56))

        # Air Density (constant)
        self._airDensity = float(vars.get('airDensity', 1.225))

        # Total of forces acting on kart
        self._forceTotal = float(vars.get('forceTotal', 10))

        # Clutch slip as percentage
        self._clutchSlip = float(vars.get('clutchSlip', 1.0))
        
        # Driven Wheel Circumfrance
        self._drivenWheelCir = float(vars.get('drivenWheelCir', math.pi * self._wheelDia))

        # Engine State
        self._state = vars.get('state', EngineState.ON) 

    def simulate_distance_run(self, until:int, step:float, throttle:int)->bool:
        """
            Method to simulate a Go-Kart run until a distance at a static throttle

            until:    measure of meters to go
            step:     time step (increment)
            throttle: throttle percentage divisible by 10
        """
        
        try:
            fname = "distance_run_" + str('%.3f' % step).split('.')[1] + "ms.txt"

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
            bsfc = 0
            torque = self._outputTorque

            # Main Loop
            while (dist < until):

                # Calculated
                kAccel = (((torque * self._spRatio * 2) / self._wheelDia) - self._forceTotal - drag) / self._kMass # mph
                velSpeed = velSprint + kAccel * step # meters / second
                dist += velSpeed * step # meters
                drag = (velSpeed ** 2) * self._airDensity * self._dragCoefficent * self._frontal / 2 # Drag Coefficient
                clutchSpeed = velSpeed * 60 * self._spRatio / self._drivenWheelCir 
                slip = (rpm - clutchSprint) / rpm
                deltaBSFC = calcBSFC(int(rpm), int(throttle)) * calcPower(int(rpm), int(throttle)) * step
                bsfc += deltaBSFC

                # for slip < 0 we need to look up engine speeed using the clutchSpeed. Look up outputTorque == engine torque.
                # if lockup == true or slip below 0 look up the table.
                if (lockup == True or slip <= 0):
                    lockup = True

                    rpm = clutchSpeed
                    
                    # Lookup torque value
                    torque = calcTorque(rpm, throttle)
                
                
                # Output
                output.append([round(timeSum, self._dLim), round(kAccel, self._dLim), round(velSpeed, self._dLim), round(dist, self._dLim), round(slip, self._dLim), round(bsfc, self._dLim), round(rpm, self._dLim), round(self._outputTorque, self._dLim)])

                # Iterate Variables
                velSprint = velSpeed
                distSprint = dist

                clutchSprint = clutchSpeed
                timeSum += step

            # Finally
            with open('runs/' + fname, 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(["Time Step", "Kart Accel", "Vehicle Speed", "Total Distance", "Clutch Slip", "BSFC", "RPM", "Torque"])
                for iteration in output:
                    filewriter.writerow(iteration)
            return True
        except Exception as e:
            raise e
            print(str(e))
            return False

    def simulate_fuel_run(self, startSpeed:float, topSpeed:float, until:float, step:float, throt:int)->bool:
        """
            Method to simulate a Go-Kart run up to full speed and coasting to a certain speed

            startSpeed: beginning speed
            topSpeed:   speed to kill the engine at
            until:      speed to stop run at
            step:       time step (increment)
            throt:      throttle percentage divisible by 10
        """
        
        try:
            fname = "fuel_run_" + str('%.3f' % step).split('.')[1] + "ms.txt"

            #Starting Values
            drag = 0
            output = []
            dist = 0
            velSprint = startSpeed
            distSprint = 0	
            clutchSprint = 0
            rpm = 2000
            timeSum = 0
            bsfc = 0
            torque = self._outputTorque
            goalReached = False
            state = EngineState.ON
            throttle = throt

            # Main Loop
            while (goalReached == False):

                # Calculated
                kAccel = (((torque * self._spRatio * 2) / self._wheelDia) - self._forceTotal - drag) / self._kMass # mph
                # kAccel = kAccel if (state == EngineState.ON) else -1 * kAccel
                velSpeed = velSprint + kAccel * step # meters / second
                dist += velSpeed * step # meters
                drag = (velSpeed ** 2) * self._airDensity * self._dragCoefficent * self._frontal / 2 # Drag Coefficient
                clutchSpeed = velSpeed * 60 * self._spRatio / self._drivenWheelCir 
                slip = (rpm - clutchSprint) / rpm
                if (state == EngineState.ON):
                    deltaBSFC = calcBSFC(int(rpm), int(throttle)) * calcPower(int(rpm), int(throttle)) * step
                    bsfc += deltaBSFC

                # for slip < 0 we need to look up engine speeed using the clutchSpeed. Look up outputTorque == engine torque.
                # if slip below 0 look up the table.
                if (slip <= 0):
                    rpm = int(clutchSpeed)
                    
                    # Lookup torque value
                    torque = calcTorque(rpm, throttle)
                
                # Output
                output.append([round(timeSum, self._dLim), round(velSpeed, self._dLim), round(dist, self._dLim), round(bsfc*100, self._dLim), round(deltaBSFC, self._dLim)])

                # Iterate Variables
                velSprint = velSpeed
                distSprint = dist

                clutchSprint = clutchSpeed
                timeSum += step


                # Check Vehicle Speed
                if (velSpeed >= topSpeed):
                    state = EngineState.OFF
                    throttle = 0
                
                if (velSpeed <= until and state == EngineState.OFF):
                    goalReached = True

                
            # Finally
            with open('runs/' + fname, 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(["Time Step", "Vehicle Speed", "Total Distance", "Total BSFC", "BSFC"])
                for iteration in output:
                    filewriter.writerow(iteration)
            return True
        except Exception as e:
            raise e
            print(str(e))
            return False


# Simulate Go-Kart Runs
# Generate CSV Files in runs folder
s = SimulateRun()
print(s.simulate_fuel_run(0, 10, 3, .05, 100))
#print(s.simulate_distance_run(100, .5, 100))
#print(s.simulate_distance_run(100, .25, 100))
#print(s.simulate_distance_run(100, .05, 100))