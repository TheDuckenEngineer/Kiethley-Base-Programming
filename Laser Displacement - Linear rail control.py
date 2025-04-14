"""****************************Imports****************************"""
import socket; import time; import pandas as pd
from keithley_base.keithley_connect import *
from keithley_base.keithley_setup import *
from keithley_base.functions import *
import serial


"""****************************Functions****************************"""
def PrintCommand(ser, command):
  # encode text to ascii
  ser.write(str.encode(command)) 

  # check for the final read out
  while True:
    line = ser.readline()
    if line == b'ok\n' or line == b'ok \n' or line == b'':
      break

def EPICFinder(s, ser, stepSize):
    # begin data collection
    InstrumentWrite(s,"INIT")
    time.sleep(0.25)
    print('Termination Criteria, Laser Displacement')

    while True:
        bufferSize = int(InstrumentQuery(s, "TRACe:ACTual? \"Sensing\"", 16).rstrip())
        
        # let the buffer get to 200 data points. if the buffer isn't large enough, pass
        if bufferSize <= 200:
            pass    
        elif bufferSize > 200:
                time.sleep(0.2)
                # read the buffer value and the average
                buffer = float(InstrumentQuery(s, f"TRACe:DATA? {bufferSize}, {bufferSize}, \"Sensing\", READ", 16).split(',')[0])
                bufferAverage = float(InstrumentQuery(s, "TRACe:STATistics:AVERage? \"Sensing\"", 16))
                print(np.round(bufferAverage, 6), buffer)
                
                # termination is when the laser displacement sees variance above the average. at termination, the actuator
                # moves back one step. future steps are cut in half. this is occurs two times before reaching zero. 
                if np.abs(bufferAverage - buffer) <= 0.1:
                    PrintCommand(ser, f'G1 F200 Z{stepSize} \n')
                else:
                    PrintCommand(ser, f'G1 F200 Z{-stepSize} \n')
                    break

    InstrumentWrite(s,"ABORT")


"""****************************Device connnection****************************"""
# define the instrament's IP address. the port is 5025 for LAN connection.
ipAddress = "169.254.253.110"
myPort = 5025

# establish connection to the LAN socket. initialize and connect to the Keithley
s = socket.socket()                 # Establish a TCP/IP socket object
InstrumentConnect(s, ipAddress, myPort, 10000)

# connect to the 3d printer
ser = serial.Serial('COM6', 115200, timeout = 1)
time.sleep(1)
PrintCommand(ser, "G28 Z \n")

# run the code until the program ends or ctr+C is hit.
try: 
    """***************Test parameters***************"""
    # input the gel type and its plasticizer content
    # print('List the gel type, plasticizer content, type, and % \n Ex: P8 XkV Xmm 5mL Xtrial')
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

    # find the EPIC boundary. set the rail to relative position mode then move until we find the boundary.
    PrintCommand(ser,f'G91 \n')
    EPICFinder(s, ser, 0.5)
    PrintCommand(ser, f'G1 F200 Z-1 \n')
    EPICFinder(s, ser, 0.01)
    print("\n Begin Test \n")

    # begin data collection for at least 10 minutes
    InstrumentWrite(s,"INIT")
    time.sleep(0.025)

    # set the printer to absolute mode and zero the z axis. move the printer slowly back and forth
    PrintCommand(ser, "G90 \n")
    PrintCommand(ser, "G92 Z0 \n")
    PrintCommand(ser, "G1 Z45 F100 \n")
    PrintCommand(ser, "G1 Z0 F100 \n")
    PrintCommand(ser, "G1 Z45 F100 \n")
    time.sleep(600)
    Data = KeithleyStop(s, numberOfChannels)
    

    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Position (mm)", "Height (mm)"])

    # convert time to displacement. the rail moves at 100 mm/min or 100/60 mm/s
    df["Position (mm)"] = Data[:, 0]*100/60
    df["Height (mm)"] = 2.49982*Data[:, 1] - 2.39379 # laser displacement sensor calibration from V to mm

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')

except KeyboardInterrupt:
    Data = KeithleyStop(s, numberOfChannels)
    
    
    """****************************Data export****************************"""
    # export the data 
    df = pd.DataFrame(columns = ["Position (mm)", "Height (mm)"])

    # convert time to displacement. the rail moves at 100 mm/min or 100/60 mm/s
    df["Position (mm)"] = Data[:, 0]*100/60
    df["Height (mm)"] = 2.49982*Data[:, 1] - 2.39379 # laser displacement sensor calibration from V to mm

    df.to_csv(f"Data/{Parameters}.csv", sep = ',', header = True, index = False)
    print('\nTest finished')
    pass