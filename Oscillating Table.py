"""****************************Imports****************************"""
import socket; import time; import pandas as pd
from keithley_base.keithley_connect import *
from keithley_base.keithley_setup import *
from keithley_base.functions import *


"""****************************Device connnection****************************"""
# define the instrament's IP address. the port is 5025 for LAN connection.
ipAddress = "169.254.139.124"
myPort = 5025

# establish connection to the LAN socket. initialize and connect to the Keithley
s = socket.socket()                 # Establish a TCP/IP socket object
InstrumentConnect(s, ipAddress, myPort, 10000)

# run the code until the program ends or ctr+C is hit.
try: 
    """***************Test parameters***************"""
    # input the gel type and its plasticizer content
    print('Input material parameters and objective for file name')
    Parameters = input('     ').upper()


    """***************Channel setup***************"""
    # list the channels used and initize the keithley. the you place these values is 
    # the order the columns will produce the excel sheet
    channels = '220' 

    # setup the channels
    KeithleySetup(s, channels)
    DcDigiVoltSetup(s, channels)
    numberOfChannels = len(channels.split(','))

    # begin data collection for at least 10 minutes
    InstrumentWrite(s,"INIT")
    time.sleep(600)
    Data = KeithleyStop(s, numberOfChannels)
    

    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Time (s)", "Voltage (V)"]) #, "Time Laser (s)", "Laser Displacement (mm)"])

    df["Time (s)"] = Data[:, 0]
    df["Voltage (V)"] = Data[:, 1]
    # df["Time Laser (s)"] = Data[:, 2]
    # df["Laser Displacement (mm)"] = Data[:, 3]

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')

except KeyboardInterrupt:

    Data = KeithleyStop(s, numberOfChannels)

    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Time (s)", "Voltage (V)"]) #, "Time Laser (s)", "Laser Displacement (mm)"])

    df["Time (s)"] = Data[:, 0]
    df["Voltage (V)"] = Data[:, 1]
    # df["Time Laser (s)"] = Data[:, 2]
    # df["Laser Displacement (mm)"] = Data[:, 3]

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')
    pass
    