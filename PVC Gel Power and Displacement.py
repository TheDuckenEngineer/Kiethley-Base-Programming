"""****************************Imports****************************"""
from keithley_base.keithley_connect import *
from keithley_base.keithley_setup import *
from keithley_base.functions import *
import socket; import pandas as pd
import time; 

"""****************************Device connnection****************************"""
# define the instrament's IP address. the port is always 5025 for LAN connection.
ip_address = "169.254.253.110"
my_port = 5025

# establish connection to the LAN socket. initialize and connect to the Keithley
s = socket.socket() # Establish a TCP/IP socket object
InstrumentConnect(s, ip_address, my_port, 10000)

# run the code until the program ends or ctr+C is hit.
try: 
    """***************Test parameters***************"""
    # input the gel type and its plasticizer content
    # print('List the gel type, plasticizer content, type, and % \n Ex: PVC P2 [N,U, or R]0.0%')
    print('Name the PVC concentration, stacked height, and input function \n Ex:PVC PX SX [cyclic or step]')
    Parameters = input('     ').upper()


    """***************Channel setup***************"""
    # list the channels used and initize the keithley. the you place these values is 
    # the order the columns will produce the excel sheet
    # 118 - voltage monitor, 119 - current monitor, 120 - laser displacement 
    channels = '118, 119, 120' 
    
    # setup the channels
    KeithleySetup(s, channels)
    DcVoltSetup(s, channels) # linear amplifier input voltage
    numberOfChannels = len(channels.split(','))

    # begin data collection for at least 10 minutes
    InstrumentWrite(s,"INIT")
    time.sleep(600)
    Data = KeithleyStop(s, numberOfChannels)
    
    """****************************Data export****************************"""
    # export the data
    df = pd.DataFrame(columns = ["Voltage Time (s)", "Voltage (V)", "Amps Time (s)", "Amps (mA)", "Displacement Time (s)", "Displacement (mm)"])

    df["Voltage Time (s)"] = Data[:, 0]
    df["Voltage (V)"] = Data[:, 1]
    df["Amps Time (s)"] = Data[:, 2]
    df["Amps (mA)"] = 2*Data[:, 3] # linear amplifier signal calibation 2mA/V 
    df["Displacement Time (s)"] = Data[:, 4]
    df["Displacement (mm)"] = 2.49982*Data[:, 5] - 2.39379 # laser displacement sensor calibration from V to mm
    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
   
    print('\nTest Finished \n\n')
    
except KeyboardInterrupt:
    Data = KeithleyStop(s, numberOfChannels)
    
    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Voltage Time (s)", "Voltage (V)", "Amps Time (s)", "Amps (mA)", "Displacement Time (s)", "Displacement (mm)"])

    df["Voltage Time (s)"] = Data[:, 0]
    df["Voltage (V)"] = Data[:, 1]
    df["Amps Time (s)"] = Data[:, 2]
    df["Amps (mA)"] = 2*Data[:, 3] # linear amplifier signal calibation 2mA/V 
    df["Displacement Time (s)"] = Data[:, 4]
    df["Displacement (mm)"] = 2.49982*Data[:, 5] - 2.39379 # laser displacement sensor calibration from V to mm
    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
   
    print('\nTest Finished \n\n')
    pass