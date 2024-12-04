from keithley_base.keithley_connect import InstrumentWrite


"""***************KEITHLEY SET UP***************"""
def KeithleySetup(s,channels):
    InstrumentWrite(s, "*RST")

    # clears the buffer, creates the sensing buffer, and assigns all data to the buffer
    InstrumentWrite(s, f"TRAC:MAKE \"Sensing\", 6000000")
    InstrumentWrite(s, f"TRACe:CLEar \"Sensing\"")
    InstrumentWrite(s, f":TRAC:FILL:MODE CONT, \"Sensing\"")
    InstrumentWrite(s, f":ROUT:SCAN:BUFF \"Sensing\"")
    
    # define the scan list, set scan count to infinite, and a channel delay of 100 us 
    InstrumentWrite(s, f":ROUTe:SCAN:CRE (@{channels})")
    InstrumentWrite(s, f":ROUT:SCAN:COUN:SCAN 0")
    InstrumentWrite(s, f":ROUT:DEL 0.0001, (@{channels})")
    
    # # set the instrament percision to 10. 6 bytes are needed for the decimal point, and formats. 
    InstrumentWrite(s, ":FORM:ASC:PREC DEF")

    # enable the graph and plot the data
    InstrumentWrite(s, f":DISP:SCR HOME")
    InstrumentWrite(s, f":DISP:WATC:CHAN (@{channels})") 
    InstrumentWrite(s, f":DISP:SCR GRAP")
    return


"""***************CHANNEL SET UP***************"""
def DcVoltSetup(s,channels):
    # define the channel function
    InstrumentWrite(s, f"FUNC 'VOLT:DC', (@{channels})")

    # set range to 1 volt, autozero off, and line sync on
    InstrumentWrite(s, f"VOLT:DC:RANG:AUTO On, (@{channels})")
    InstrumentWrite(s, f"VOLT:DC:AZER OFF, (@{channels})")
    InstrumentWrite(s, f"VOLT:DC:LINE:SYNC ON, (@{channels})")
    return


def ResistanceSetup(s,channels):
    # define the channel function
    InstrumentWrite(s, f"FUNC 'RES', (@{channels})")

    # turn autozero on and line sync on
    InstrumentWrite(s, f"RES:AZER OFF, (@{channels})")
    InstrumentWrite(s, f"RES:LINE:SYNC ON, (@{channels})")
    return


def ThermoSetup(s,channels):
    # define the channel function
    InstrumentWrite(s, f"FUNC 'TEMP', (@{channels})")

    # set reading thermocouple, type K, read in celcius, dont 
    # dont check for broken wire, use a internal temperature at 26-29 C,
    # enable autozero and turn on line sync
    InstrumentWrite(s, f"TEMP:TRAN TC, (@{channels})")
    InstrumentWrite(s, f"TEMP:TC:TYPE K, (@{channels})")
    InstrumentWrite(s, f"TEMP:UNIT CELS, (@{channels})")
    InstrumentWrite(s, f"TEMP:ODET OFF, (@{channels})")
    InstrumentWrite(s, f"TEMP:TC:RJUN:RSEL INT, (@{channels})")
    InstrumentWrite(s, f"TEMP:TC:RJUN:SIM 28.5, (@{channels})")    
    InstrumentWrite(s, f"TEMP:AZER ON, (@{channels})")
    InstrumentWrite(s, f"TEMP:LINE:SYNC ON, (@{channels})")
    return


def CapacitorSetup(s,channels):
    # define the channel function
    InstrumentWrite(s, f"FUNC 'CAP', (@{channels})")

    # set the capacitors range if needed
    # InstrumentWrite(s, f"CAP:RANG 1, (@{channels})")
    return
