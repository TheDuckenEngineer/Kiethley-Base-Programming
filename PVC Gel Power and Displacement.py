"""****************************Imports****************************"""
from keithley_base.keithley_connect import *
from keithley_base.keithley_setup import *
import socket; import numpy as np; import pandas as pd
import time; 

"""****************************Device connnection****************************"""
# define the instrament's IP address. the port is always 5025 for LAN connection.
ip_address = "169.254.253.110"
my_port = 5025

# establish connection to the LAN socket. initialize and connect to the Keithley
s = socket.socket() # Establish a TCP/IP socket object
instrument_connect(s, ip_address, my_port, 10000)

# run the code until the program ends or ctr+C is hit.
try: 
    """***************Test parameters***************"""
    # input the gel type and its plasticizer content
    # print('List the gel type, plasticizer content, type, and % \n Ex: PVC P2 [N,U, or R]0.0%')
    print('Name the PVC concentration, stacked height, and input function \n Ex:PVC PX SX [cyclic or step]')
    Parameters = input('     ').upper()


    """***********************Data matrices***********************"""
    # preallocate the data collection matrices
    buffer = np.zeros(0)
    bufferTimes = np.zeros(0)


    """***************Channel setup***************"""
    # list the channels used and initize the keithley. the you place these values is 
    # the order the columns will produce the excel sheet
    # 118 - voltage monitor, 119 - amp monitor, 120 - laser displacement 
    channels = '118, 119, 120' 
    
    # setup the channels
    KeithleySetup(s, channels)
    DcVoltSetup(s, channels) # linear amplifier input voltage
    numberOfChannels = len(channels.split(','))

    # begin data collection for at least 10 minutes
    instrument_write(s,"INIT")
    time.sleep(600)

except KeyboardInterrupt:
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
    
    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Time (s)", "Voltage (V)", "Time (s)", "Amps (mA)", "Time (s)", "Laser Displacement (mm)"])

    df["Time (s)"] = Data[:, 0]
    df["Voltage (V)"] = Data[:, 1]
    df["Time (s)"] = Data[:, 2]
    df["Amps (mA)"] = 0.5*Data[:, 3] # linear amplifier signal calibation 0.5V/mA 
    df["Time (s)"] = Data[:, 4]
    df["Laser Displacement (mm)"] = 2.49982*Data[:,-1] - 2.39379 # laser displacement sensor calibration from v to mm
    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
   
    print('\nTest Finished \n\n')
    pass