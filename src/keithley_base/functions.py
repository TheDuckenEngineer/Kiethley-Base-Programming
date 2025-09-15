from keithley_base.keithley_connect import *
import numpy as np  

def KeithleyStop(s, numberOfChannels):
    
    # read the Keithley buffer by groups of measurements. This needs to be a 
    # double multiplicly of the number of channels. 
    if numberOfChannels > 1:
        collectionSize = int(220 - 200%numberOfChannels**2)/numberOfChannels**2
    else:
        collectionSize = 30

    # preallocate the data collection matrices
    measurement = np.zeros(0, dtype = float)
    
    # stop the Keithley at an integer value of the data collected
    while True:
        bufferSize = int(InstrumentQuery(s, "TRACe:ACTual:END? \"Sensing\"", 16).rstrip())
        if bufferSize % numberOfChannels == 0:
            InstrumentWrite(s, "ABORT")
            break
        else:
            pass
        
    # collect the data from the buffer
    print('Reading buffer\n')
    index = np.arange(1, bufferSize, collectionSize) 
    for i in range(0, len(index) - 1):
        # read the measurements and their realtive times
        buffer = np.float64(np.array(InstrumentQuery(s, f"TRACe:DATA? {index[i]}, {index[i + 1] - 1}, \"Sensing\", REL, READ", 16*bufferSize).split(',')))
        measurement = np.hstack([measurement, buffer])

    Data = measurement.reshape(int(len(measurement)/2/numberOfChannels), 2*numberOfChannels)
    
    return Data