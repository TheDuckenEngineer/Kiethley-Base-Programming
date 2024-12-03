"""****************************Imports****************************"""
import socket; import time; import pandas as pd
from keithley_base.keithley_connect import *
from keithley_base.keithley_setup import *
from keithley_base.functions import *


"""****************************Device connnection****************************"""
# define the instrament's IP address. the port is 5025 for LAN connection.
ip_address = "169.254.253.110"
my_port = 5025

# establish connection to the LAN socket. initialize and connect to the Keithley
s = socket.socket()                 # Establish a TCP/IP socket object
instrument_connect(s, ip_address, my_port, 10000)

# run the code until the program ends or ctr+C is hit.
try: 
    """***************Test parameters***************"""
    # input the gel type and its plasticizer content
    # print('List the gel type, plasticizer content, type, and % \n Ex: PVC P2 [N,U, or R]0.0%')
    print('Input material parameters and objective for file name')
    Parameters = input('     ').upper()


    """***************Channel setup***************"""
    # list the channels used and initize the keithley. the you place these values is 
    # the order the columns will produce the excel sheet
    channels = '120' 

    # setup the channels
    KeithleySetup(s, channels)
    DcVoltSetup(s, channels)
    numberOfChannels = len(channels.split(','))

    # begin data collection for at least 10 minutes
    instrument_write(s,"INIT")
    time.sleep(600)
    Data = KeithleyStop(s, numberOfChannels)
    

    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Time (s)", "Laser Displacement (mm)"])

    df["Time (s)"] = Data[:, 0]
    df["Laser Displacement (mm)"] = 2.49982*Data[:, 1] - 2.39379 # laser displacement sensor calibration from V to mm

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')

except KeyboardInterrupt:
    Data = KeithleyStop(s, numberOfChannels)
    
    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Time (s)", "Laser Displacement (mm)"])

    df["Time (s)"] = Data[:, 0]
    df["Laser Displacement (mm)"] = 2.49982*Data[:, 1] - 2.39379 # laser displacement sensor calibration from V to mm

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')
    pass