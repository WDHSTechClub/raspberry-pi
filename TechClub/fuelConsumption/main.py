import math
import sys
try: 
    import tkinter
    from tkinter import *
    tk=tkinter.Tk()
except:
    try:
        import Tkinter
        from Tkinter import *
        tk=Tkinter.Tk()
    except:
        print("No Tkinter or tkinter!")
        sys.exit()

tk.title("Data Entry")
area = []
dragCoefficent = []
clutchInit = []
clutchMin = []
rollingResistance = []
goKartMass = []
frontSprocketTeeth = []
rearSprocketTeeth = []
throttle = []
timeStep = []
wheelDiameter = []
airDensity = []
dataEntryStepper = 0

t50throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (0.77, 0.12),#, 43.1034),
    (1.44, 0.24),#, 4.3103),
    (2.03, 0.36),#, 8.5676),
    (2.56, 0.48),#, 0.4310),
    (3.03, 0.60),#, 0.2155),
    (3.45, 0.72),#, 0.1437),
    (3.50, 0.77),#, 0.1437),
    (3.54, 0.82),#, 0.1437),
    (3.58, 0.86),#, 0.1197),
    (3.62, 0.91),#, 0.1197),
    (3.65, 0.96),#, 0.1197),
    (3.65, 0.99),#, 0.1197),
    (3.65, 1.03),#, 0.1197),
    (3.65, 1.07),#, 0.1197),
    (3.65, 1.11),#, 0.1197),
    (3.65, 1.15),#, 0.1197),
    (2.94, 0.96),#, 0.1197),
    (2.28, 0.76),#, 0.1437),
    (1.66, 0.57),#, 0.1437),
    (1.07, 0.38),#, 0.2155),
    (0.58, 0.19),#, 0.4310),
    (0.00, 0.00),#, 0.4310]
]

t60throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (0.92, 0.14),#, 43.1034),
    (1.73, 0.29),#, 4.3103),
    (2.44, 0.43),#, 0.4310),
    (3.07, 0.58),#, 0.4310),
    (3.63, 0.72),#, 0.2155),
    (4.14, 0.87),#, 0.1437),
    (4.20, 0.92),#, 0.1437),
    (4.25, 0.98),#, 0.1197),
    (4.30, 1.03),#, 0.1197),
    (4.34, 1.09),#, 0.1197),
    (4.38, 1.15),#, 0.1078),
    (4.38, 1.19),#, 0.1078),
    (4.38, 1.24),#, 0.1078),
    (4.38, 1.28),#, 0.1078),
    (4.38, 1.33),#, 0.1078),
    (4.38, 1.38),#, 0.1078),
    (3.89, 1.26),#, 0.1197),
    (3.42, 1.15),#, 0.1197),
    (2.99, 1.03),#, 0.1437),
    (2.58, 0.92),#, 0.1437),
    (2.19, 0.80),#, 0.2155),
    (1.83, 0.69),#, 0.2155),
]

t70throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (1.07, 0.17),#, 43.1034),
    (2.01, 0.34),#, 4.3103),
    (2.84, 0.51),#, 0.4310),
    (3.58, 0.67),#, 0.4310),
    (4.24, 0.84),#, 0.4310),
    (4.83, 1.01),#, 0.2155),
    (4.90, 1.08),#, 0.1437),
    (4.96, 1.14),#, 0.1437),
    (5.01, 1.21),#, 0.1197),
    (5.06, 1.27),#, 0.1197),
    (5.11, 1.34),#, 0.1078),
    (5.11, 1.39),#, 0.1078),
    (5.11, 1.44),#, 0.1078),
    (5.11, 1.50),#, 0.1078),
    (5.11, 1.55),#, 0.1078),
    (5.11, 1.61),#, 0.1078),
    (4.75, 1.54),#, 0.1078),
    (4.41, 1.48),#, 0.1197),
    (4.09, 1.41),#, 0.1197),
    (3.79, 1.35),#, 0.1197),
    (3.50, 1.28),#, 0.1437),
    (3.24, 1.22),#, 0.1437),
]

t80throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (1.23, 0.19),#, 43.1034),
    (2.30, 0.39),#, 4.3103),
    (3.25, 0.58),#, 0.4310),
    (4.09, 0.77),#, 0.2155),
    (4.84, 0.96),#, 0.1437),
    (5.52, 1.16),#, 0.1437),
    (5.60, 1.23),#, 0.1197),
    (5.67, 1.31),#, 0.1197),
    (5.73, 1.38),#, 0.1078),
    (5.79, 1.45),#, 0.1078),
    (5.84, 1.53),#, 0.0958),
    (5.84, 1.59),#, 0.0958),
    (5.84, 1.65),#, 0.0958),
    (5.84, 1.71),#, 0.0958),
    (5.84, 1.77),#, 0.0958),
    (5.84, 1.83),#, 0.1078),
    (5.54, 1.80),#, 0.1078),
    (5.26, 1.76),#, 0.1197),
    (4.99, 1.72),#, 0.1197),
    (4.74, 1.69),#, 0.1197),
    (4.51, 1.65),#, 0.1437),
    (4.28, 1.61),#, 0.1437),
]

t90throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (1.38, 0.22),#, 43.1034),
    (2.59, 0.43),#, 4.3103),
    (3.56, 0.65),#, 0.4310),
    (4.60, 0.87),#, 0.2155),
    (5.45, 1.08),#, 0.1437),
    (6.21, 1.30),#, 0.1437),
    (6.30, 1.38),#, 0.1197),
    (6.37, 1.47),#, 0.1197),
    (6.44, 1.55),#, 0.1078),
    (6.51, 1.64),#, 0.0958),
    (6.57, 1.72),#, 0.0862),
    (6.57, 1.79),#, 0.0862),
    (6.57, 1.86),#, 0.0958),
    (6.57, 1.93),#, 0.0958),
    (6.57, 2.00),#, 0.0958),
    (6.57, 2.06),#, 0.1078),
    (6.29, 2.04),#, 0.1078),
    (6.04, 2.02),#, 0.1078),
    (5.79, 2.00),#, 0.1197),
    (5.57, 1.98),#, 0.1197),
    (5.35, 1.96),#, 0.1437),
    (5.15, 1.94),#, 0.1437),
]

t100throttleArray = [
    (0.00, 0.00),#, 431.0345),
    (1.53, 0.24),#, 43.1034),
    (2.88, 0.48),#, 4.3103),
    (4.06, 0.72),#, 0.4310),
    (5.11, 0.96),#, 0.2155),
    (6.05, 1.20),#, 0.2155),
    (6.90, 1.45),#, 0.1437),
    (7.00, 1.54),#, 0.1197),
    (7.08, 1.63),#, 0.1197),
    (7.16, 1.72),#, 0.1078),
    (7.23, 1.82),#, 0.0958),
    (7.30, 1.91),#, 0.0862),
    (7.30, 1.99),#, 0.0647),
    (7.30, 2.06),#, 0.0862),
    (7.30, 2.14),#, 0.0958),
    (7.30, 2.22),#, 0.0958),
    (7.30, 2.29),#, 0.0958),
    (7.22, 2.34),#, 0.1078),
    (7.15, 2.40),#, 0.1078),
    (7.08, 2.45),#, 0.1197),
    (7.02, 2.50),#, 0.1197),
    (6.95, 2.55),#, 0.1437),
    (6.90, 2.60),#, 0.1437)
]

class DataEntry(object):
    def __init__(self, title, default):
        global dataEntryStepper
        self.entries = {}
        self.title = title
        self.default = default
        self.index = dataEntryStepper
        t = Label(tk, text = self.title + ":")
        t.grid(row = self.index, column = 0)
        self.entries["0"] = Entry(tk)
        self.entries["0"].delete(0,END)
        self.entries["0"].insert(0,default)
        self.entries["0"].grid(row = self.index, column = 1)
        self.button = Button(tk, text = "+", command = self.buttonFunct)
        self.button.grid(row = self.index, column = 2)
        dataEntryStepper += 1
    def buttonFunct(self):
        self.entries[str(len(self.entries))] = Entry(tk)
        self.entries[str(len(self.entries) - 1)].delete(0, END)
        self.entries[str(len(self.entries) - 1)].insert(0, self.entries["0"].get())
        self.entries[str(len(self.entries) - 1)].grid(row = self.index, column = (len(self.entries)))
        self.button.grid(row = self.index, column = (len(self.entries) + 1))
    def get(self):
        out = []
        for i in self.entries:
            out.append(self.entries[i].get())
        return out

class Math:
    def __init__(self, spFront, spRear, rpm, engineTorque, velocity, dragCoefficient, wheelDiameter, interval, engPW, time, speed, throttle):
        self.spFront = spFront
        self.spRear = spRear
        self.engineTorque = engineTorque
        self.rpm = rpm
        self.velocity = velocity
        self.dragCoefficient = dragCoefficient
        self.wheelDiameter = wheelDiameter
        self.interval = interval
        self.engPW = engPW
        self.time = time
        self.speed = speed
        self.weir = wheelDiameter * math.pi
        self.throttle = throttle
        
    def doMath(s):
        self.spRatio = self.spRatio(self.spFront, self.spRear)
        self.engineSpeed = self.clutchOutputTorque(throttle, rpm)
        #self.engineSpeed = self.engineSpeed(0) #Get intercept of eng torque and clutch torque
        self.finalClutch = self.finalClutchOutputSpeed(self.speed, self.time, self.weir)
        self.clutchSlip = self.clutchSlip(self.finalClutch, self.rpm)
        self.windResistence = self.windResistence(self.velocity, self.dragCoefficient)
        self.totalRolling = self.totalRollingDistance(self.windReistence)
        self.kAccel = self.kartAccelWithClutch(self.engineSpeed, self.spRatio, self.wheelDiameter)
        self.finalSpeed = self.vehicleFinalSpeed(self.kAccel, self.interval)
        # Fcon = Fcon1 + Fcon = 0.1042g + 0.1042g = 0.2084
        intercept = self.clutchOutputTorque(self.throttle, self.rpm)
        
    @staticmethod
    def spRatio(spFront, spRear):
        """
        spRatio = Sprear / Spfront = 7.0833
        ~ Spfront = # teeth on front sprocket
        ~ Sprear = # teeth on rear sprocket
        """
        spRatio = spRear / spFront
        return spRatio

    @staticmethod
    def clutchOutputTorque(throttle, rpm):
        """
        ct = Engt @ 100% throttle; 2000 (rpm)
        ~ Engt = Engine Torque (Nm)
        """
        if throttle > 100 or throttle < 0:
            return "Error; Throttle out of range!"
        else:
            if throttle == 100:
               throttleArray = t100throttleArray
            elif throttle == 90:
                throttleArray = t90throttleArray
            elif throttle == 80:
                throttleArray = t80throttleArray
            elif throttle == 70:
                throttleArray = t70throttleArray
            elif throttle == 60:
                throttleArray = t60throttleArray
            elif throttle == 50:
                throttleArray = t50throttleArray
            else:
                return "Error; Throttle out of range."
            rpmValues = []
            clutchTorqueLine = []
            rpmRound = int(rpm/100)
            index = rpmRound-14
            clutchPoint = (throttleArray[index-1], throttleArray[index])
            for i in range(1400, 3700, 100):
                rpmValues.append(i)
            for i in range(len(rpmValues)):
                clutchTorque = 0.014 * rpmValues[i] - 20.7
                if clutchTorque < 0:
                    clutchTorque = 0
                clutchTorqueLine.append((clutchTorque, rpmValues[i]))
            xint = (-(clutchPoint[0][1] - ((clutchPoint[1][1] - clutchPoint[0][1]) / (clutchPoint[1][0] - clutchPoint[0][0])) * clutchPoint[0][0] + 20.7) / (((clutchPoint[1][1] - clutchPoint[0][1]) / (clutchPoint[1][0] - clutchPoint[0][0])) - .014))
            yint = (((clutchPoint[1][1] - clutchPoint[0][1]) / (clutchPoint[1][0] - clutchPoint[0][0])) * (-clutchPoint[0][1] - ((clutchPoint[1][1] - clutchPoint[0][1]) / (clutchPoint[1][0] - clutchPoint[0][0])) * clutchPoint[0][0] + 20.7) + (clutchPoint[0][1] - ((clutchPoint[1][1] - clutchPoint[0][1]) / (clutchPoint[1][0] - clutchPoint[0][0])) * clutchPoint[0][0]))
            intercept = [xint, yint]
            for x in range(len(intercept)):
                if intercept[x] < 0:
                    intercept[x] = math.fabs(intercept[x])
            return clutchPoint, intercept

    @staticmethod
    def clutchIntercept(throttle):
        """
        ct = Engt @ 100% throttle; 2000 (rpm)
        ~ Engt = Engine Torque (Nm)
        """
        if throttle > 100 or throttle < 0:
            return "Error; Throttle out of range!"
        else:
            if throttle == 100:
               throttleArray = t100throttleArray
            elif throttle == 90:
                throttleArray = t90throttleArray
            elif throttle == 80:
                throttleArray = t80throttleArray
            elif throttle == 70:
                throttleArray = t70throttleArray
            elif throttle == 60:
                throttleArray = t60throttleArray
            elif throttle == 50:
                throttleArray = t50throttleArray
            else:
                return "Error; Throttle out of range."
            interceptX = 0
            interceptY = 0
            for x in range(len(throttleArray)):
                y = throttleArray[x][1]
                clutchX = (20.7+y)/(.014)
                if clutchX <= throttleArray[x][0]:
                    interceptX = clutchX
                    interceptY = y
                    break
                print([clutchX, y])
            print([interceptX, interceptY])
        return null
       
    @staticmethod     
    def clutchSlip(clutchOutputTorque, rpm):
        """
        Cslip = (Weng  - Cw) / (Weng) = 100%
        ~ Weng = Engine Speed (rpm)
        ~ Cw = Clutch Output Speed (rpm) --From finalClutchOutputSpeed() Formula
        """
        clutchSlip = (rpm - clutchOutputTorque) / rpm
        return clutchOutputTorque

    @staticmethod
    def windResistence(velocity, dragCoefficient, frontArea):
        """
        Fd = (0.5) * p * (V^2) * Cd * A = 0
        ~ p = Air Density = 1.225 (kg/m^2)
        ~ V = Vehicle Velocity
        ~ Cd = Drag Coefficent = 0.3 (ratio)
        ~ A = Kart Frontal Area = 0.560 (m^2)
        """
        windResistence = .5 * 1.225 * (velocity ** 2) * dragCoefficient * frontArea
        return windResistence

    @staticmethod
    def totalRollingDistance(forceAreaDrag):
        """
        Frtotal = Fd + Frr = 10 (N)
        ~ Fd = Force Area Drag = (windReistence Formula Above) = 0
        ~ Frr = Force Rolling Resistence = 10 (N)
        """
        totalRollingDistance = forceAreaDrag + 10
        return totalRollingDistance

    @staticmethod
    def kartAccelWithClutch(clutchOutputTorque, spRatio, wheelDiameter, kartMass):
        """
        Kaccel = ((Ct * Spratio * 2) / (Wdia)) / Mkart = 1.374 (m/s^2)
        ~ Ct = Clutch Output Torque = ((Nm) / (rpm))
        ~ Spratio = (Sprear / Spfront)
        ~ Wdia = Rear Wheel Diameter = 22 (in) = 0.5588 (m)
        ~ Mkart = Kart Mass = 120 (Kg)
        """
        kartAccel = ((clutchOutputTorque * spRatio * 2) / wheelDiameter) / kartMass
        return kartAccel

    @staticmethod
    def vehicleFinalSpeed(kAccel, interval):
        """
        Vsp = Kaccel * Tstep = 0.687 m/s
        ~ Kaccel = (kartAccelWithClutch Formula Above)
        ~ Tstep = Time Step (interval)
        """
        speed = kAccel * interval
        return speed

    @staticmethod
    def fuelConsumedDuringStepTime(bsfc, interval, engPW):
        """
        Fcon = BSFC * Tstep = Engpw * 0.5 (sec) * 1.45 (Kw) = 0.1042 (grams)
        ~ BSFC = Break Specif Fuel Consumption
        ~ Tstep = Time Step (interval)
        ~ Engpw = 0.1437 (g / kw * s)
        """
        fuelConsumed = bsfc * interval
        umm = engPW * .5 * 1.45
        return fuelConsumed

    @staticmethod
    def finalClutchOutputSpeed(vehicleSpeed, time, weir, spRatio):
        """
        Wsp = (Vsp * (60sec / min)) / (Weir) = 23.4 (rpm)
        ~ Vsp = Vehicle Speed (m/s)
        ~ Weir = Rear Wheel Circumfrence = Wdia * pi
        ~ Wdia = 0.5588 (m) = Rear Wheel Diameter

        Cw = Wsp * Spratio = 23.4(7.0833) = 165.89 (rpm)
        ~ Wsp = (Other Formula Above)
        ~ Spratio = (Sprear / Spfront)
        """
        wheelSpeed = (vehicleSpeed * (60 / time)) / weir
        finalClutch = wheelSpeed * spRatio
        return finalClutch

    @staticmethod
    def vehicleAcellerationTorque(wheelDiameter, torque, frontSprocket, rearSprocket, velocity, dragCoefficient, frontArea, rollingResistance, vehicleMass):
        return ((((torque * (rearSprocket / frontSprocket)) / (wheelDiameter / 2)) + windResistence(velocity, dragCoefficient, frontArea) + rollingResistance) / vehicleMass)


aE = DataEntry("Kart Frontal Area", "0.56")
dE = DataEntry("Drag Coefficent", "0.3")
c_iE = DataEntry("Clutch Init", "0.0")
c_mE = DataEntry("Clutch Min", "0.0")
r_rE = DataEntry("Rolling Resistance", "0.0")
mE = DataEntry("Vehicle Mass", "120.0")
f_sE = DataEntry("Front Sprocket Teeth", "12")
r_sE = DataEntry("Rear Sprocket Teeth", "85")
tE = DataEntry("Throttle", "0.0")
t_sE = DataEntry("Time Step", "0.1")
w_dE = DataEntry("Wheel Diameter", "0.5588")
a_dE = DataEntry("Air Density", "1.225")
rpmE = DataEntry("RPM", "1400")
def get_CheckData():
        try:
                data = {}
                
                area = aE.get()
                data["area"] = area
                
                dragCoefficent = dE.get()
                data["dragCoefficient"] = dragCoefficent
                
                clutchInit = c_iE.get()
                data["clutchInit"] = clutchInit
                
                clutchMin = c_mE.get()
                data["clutchMin"] = clutchMin
                
                rollingResistance = r_rE.get()
                data["rollingResistace"] = rollingResistance
                
                goKartMass = mE.get()
                data["mass"] = goKartMass
                
                frontSprocketTeeth = f_sE.get()
                data["frontTeeth"] = frontSprocketTeeth
                
                rearSprocketTeeth = r_sE.get()
                data["rearTeeth"] = rearSprocketTeeth
                
                throttle = tE.get()
                data["throttle"] = throttle
            
                timeStep = t_sE.get()
                data["deltaTime"] = timeStep
                
                wheelDiameter = w_dE.get()
                data["wheelDiameter"] = wheelDiameter
                
                airDensity = a_dE.get()
                data["airDensity"] = airDensity
                
                rpm = rpmE.get()
                data["rpm"] = rpm
                
                ##run more functions here or close tk window and run after
                print(data)
                tk.destroy()
        except:
                t = Label(tk, text = "Error")
                t.grid(row = 13, column = 1)
submitButton = Button(tk, text="Submit", command = get_CheckData)
submitButton.grid(row = 13)
tk.mainloop()
