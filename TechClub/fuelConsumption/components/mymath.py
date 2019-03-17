from components import arrays

def calcTorque(rpm:int, throttle:int)->float:
    """
        Method to calculate torque

        rpm:      between 1400 and 3600
        throttle: percentage divisible by 10
    """

    if (throttle == 0):
        return 0

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
    elif (rpm >= 3600):
        return float(0)
    else:
        raise LookupError('rpm out of range! -> ' + str(rpm))

def calcBSFC(rpm:int, throttle:int)->float:
    """
        Method to calculate brake specific fuel consumption

        rpm:      between 1400 and 3600
        throttle: percentage divisible by 10
    """

    if (rpm >= 1400 and rpm <= 3600):
        return findBSFC(int(rpm / 100), throttle)
    else:
        return float(0)

def calcPower(rpm:int, throttle:int)->float:
    """
        Method to calculate power

        rpm:      between 1400 and 3600
        throttle: percentage divisible by 10
    """

    if (rpm >= 1400 and rpm <= 3600):
        return findPower(int(rpm / 100), throttle)
    else:
        return float(0)

def findTorque(msbRPM:int, throttle:int)->float:
    """
        Lookup method to find torques in arrays.py

        msbRPM:   two-digit rpm (rpm / 100)
        thorttle: throttle percentage divisble by 10
    """
    # msbRPM = rpm / 100

    if ((type(msbRPM) == int) and (type(throttle) == int)):
        return findTuple(msbRPM, throttle)[0]
    else:
        raise TypeError('Type Error with _findTorque() call!')

def findPower(msbRPM:int, throttle:int)->float:
    """
        Lookup method to find powers in arrays.py

        msbRPM:   two-digit rpm (rpm / 100)
        thorttle: throttle percentage divisble by 10
    """
    # msbRPM = rpm / 100

    if ((type(msbRPM) == int) and (type(throttle) == int)):
        return findTuple(msbRPM, throttle)[1]
    else:
        raise TypeError('Type Error with _findPower() call!')

def findBSFC(msbRPM:int, throttle:int)->float:
    """
        Lookup method to find BSFC's in arrays.py

        msbRPM:   two-digit rpm (rpm / 100)
        thorttle: throttle percentage divisble by 10
    """
    # msbRPM = rpm / 100

    if ((type(msbRPM) == int) and (type(throttle) == int)):
        return findTuple(msbRPM, throttle)[2]
    else:
        raise TypeError('Type Error with _findBSFC() call!')

def findTuple(msbRPM:int, throttle:int)->tuple:
    """
        Lookup method to find tuples in arrays.py

        msbRPM:   two-digit rpm (rpm / 100)
        thorttle: throttle percentage divisble by 10
    """
    # msbRPM = rpm / 100
    print("369-", msbRPM, throttle)
    if ((type(msbRPM) == int) and (type(throttle) == int)):
        # Validate RPM Value
        if (msbRPM >= 14 and msbRPM <= 36):
            # Get Throttle Row based on RPM
            index = int(msbRPM - 14)

            # Validate Throttle Value to reduce chance of error
            if ((throttle % 10 == 0) and (throttle > 0 and throttle <= 100)):
                # Define array name to retrieve torque from based on throttle
                arrayName = str("arrays.t" + str(int(throttle)) + "throttleArray")

                # Get torque at certain throttle and RPM
                cmd = str(arrayName + "[" + str(index) + "]")
                tup = eval(cmd)
                return tup
            else:
                return (0, 0, 0)
        else:
            return (0, 0, 0)
    else:
        raise TypeError('Type Error with __findTuple() call!')