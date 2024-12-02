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
    # prealocate the iteraive fuction
    bufferInitial = 0

    # preallocate the data collection matrices
    buffer = np.zeros(0)
    bufferTimes = np.zeros(0)


    """***************Channel setup***************"""
    # list the channels used and initize the keithley. the you place these values is 
    # the order the columns will produce the excel sheet
    channels = '118, 119, 120' 
    indivChannels = channels.split(',')
    
    # setup the channels
    KeithleySetup(s, channels)
    DcVoltSetup(s, indivChannels[0]) # linear amplifier input voltage
    AmpsSetup(s, indivChannels[1]) # linear amplifier input amps
    DcVoltSetup(s, indivChannels[2]) # laser displacement voltage
    numberOfChannels = len(indivChannels)

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
    for i in range(1, bufferInitial + 1):
        # read the measurements and their realtive times
        bufferTimes = np.hstack([bufferTimes, float(np.array(instrument_query(s, f"TRACe:DATA? {i}, {i}, \"Sensing\", REL", 16*bufferSize).split(',')))])
        buffer = np.hstack([buffer, float(np.array(instrument_query(s, f"TRACe:DATA? {i}, {i}, \"Sensing\", READ", 16*bufferSize).split(',')))])
    bufferData = np.vstack([bufferTimes, buffer]).T.reshape(int(len(buffer)/numberOfChannels), 2*numberOfChannels)
        
    # create the data export matrix. adjust the final column for the laser displacement voltage to disp 
    Data = np.vstack([bufferTimes, buffer]).T
    Data[:,-1] = 2.49982*Data[:,-1] - 2.39379
    
    """****************************Data export****************************"""
    # export the data 
    # df = pd.DataFrame(columns = ["Time (s)", "Voltage (V)", "Time (s)", "Amps (A)", "Time (s)", "Laser Displacement (mm)"])

    # df["Time (s)"] = 
    # df["Voltage (V)"] = 
    # df["Amps (A)"] = 
    # df["Laser Displacement (mm)"] = 
    
    # df.to_csv(f"Power Data\{Parameters}.csv", sep = ',', header = True, index = False)
   
    print('\nTest Finished \n\n')
    pass