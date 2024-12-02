from keithley_base.keithley_connect import *
import numpy as np


def KeithleyStop(s, numberOfChannels):
    # preallocate the data collection matrices
    buffer = np.zeros(0)
    bufferTimes = np.zeros(0)
    
    # stop the Keithley at an integer value of the data collected
    while True:
        bufferSize = int(instrument_query(s, "TRACe:ACTual:END? \"Sensing\"", 16).rstrip())
        if bufferSize % numberOfChannels == 0:
            instrument_write(s, "ABORT")
            break
        else:
            pass
        
    # collect the data from the buffer
    print('Reading buffer\n')
    for i in range(1, bufferSize + 1):
        # read the measurements and their realtive times
        measurement = np.array(instrument_query(s, f"TRACe:DATA? {i}, {i}, \"Sensing\", REL, READ", 16*bufferSize).split(','))
        bufferTimes = np.hstack([bufferTimes, float(measurement[0])])
        buffer = np.hstack([buffer, float(measurement[1])])
    Data = np.vstack([bufferTimes, buffer]).T.reshape(int(len(buffer)/numberOfChannels), 2*numberOfChannels)
    return Data