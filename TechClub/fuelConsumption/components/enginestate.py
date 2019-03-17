from enum import Enum, unique

@unique
class EngineState(Enum):
    """
        Enumeration used for detirmining engine state of the Go-Kart.

        To be used with the SimulateRun class which will include a state variable
        which will be used to detirmine if the engine is on, off, or on and idle.
    """
    OFF = 0
    ON = 1
    IDLE = 2