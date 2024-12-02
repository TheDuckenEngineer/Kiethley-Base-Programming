"""****************************Imports****************************"""
import socket; import numpy as np;
import time; import os.path
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
    print('List the GO concentratioin in %, and input function \n Ex:PVC X GO 0.0% [cyclic or step]')
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

except KeyboardInterrupt:
    Data = KeithleyStop(s, numberOfChannels)
    
    """****************************Data export****************************"""
    fileName = f'PVC P4 {Parameters}'
    if os.path.isfile(fileName) == 0:
        np.savetxt(f"{fileName}.csv", Data, delimiter=",")
    elif os.path.isfile(fileName) == 1:
        os.remove(fileName)
        np.savetxt(f"{fileName}.csv", Data, delimiter=",")
    instrument_write(s, "ABORT")
    print('\nTest aborted')
    pass