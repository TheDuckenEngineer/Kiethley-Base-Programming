from keithley_base.keithley_connect import instrument_write


"""***************KEITHLEY SET UP***************"""
def KeithleySetup(s,channels):
    instrument_write(s, "*RST")

    # clears the buffer, creates the sensing buffer, and assigns all data to the buffer
    instrument_write(s, f"TRAC:MAKE \"Sensing\", 6000000")
    instrument_write(s, f"TRACe:CLEar \"Sensing\"")
    instrument_write(s, f":TRAC:FILL:MODE CONT, \"Sensing\"")
    instrument_write(s, f":ROUT:SCAN:BUFF \"Sensing\"")
    
    # define the scan list, set scan count to infinite, and a channel delay of 100 us 
    instrument_write(s, f":ROUTe:SCAN:CRE (@{channels})")
    instrument_write(s, f":ROUT:SCAN:COUN:SCAN 0")
    instrument_write(s, f":ROUT:DEL 0.0001, (@{channels})")
    
    # # set the instrament percision to 10. 6 bytes are needed for the decimal point, and formats. 
    instrument_write(s, ":FORM:ASC:PREC DEF")

    # enable the graph and plot the data
    instrument_write(s, f":DISP:SCR HOME")
    instrument_write(s, f":DISP:WATC:CHAN (@{channels})") 
    instrument_write(s, f":DISP:SCR GRAP")
    return


"""***************CHANNEL SET UP***************"""
def DcVoltSetup(s,channels):
    # define the channel function
    instrument_write(s, f"FUNC 'VOLT:DC', (@{channels})")

    # set range to 1 volt, autozero off, and line sync on
    instrument_write(s, f"VOLT:DC:RANG 1, (@{channels})")
    instrument_write(s, f"VOLT:DC:AZER OFF, (@{channels})")
    instrument_write(s, f"VOLT:DC:LINE:SYNC ON, (@{channels})")
    return


def ResistanceSetup(s,channels):
    # define the channel function
    instrument_write(s, f"FUNC 'RES', (@{channels})")

    # turn autozero on and line sync on
    instrument_write(s, f"RES:AZER OFF, (@{channels})")
    instrument_write(s, f"RES:LINE:SYNC ON, (@{channels})")
    return


def ThermoSetup(s,channels):
    # define the channel function
    instrument_write(s, f"FUNC 'TEMP', (@{channels})")

    # set reading thermocouple, type K, read in celcius, dont 
    # dont check for broken wire, use a internal temperature at 26-29 C,
    # enable autozero and turn on line sync
    instrument_write(s, f"TEMP:TRAN TC, (@{channels})")
    instrument_write(s, f"TEMP:TC:TYPE K, (@{channels})")
    instrument_write(s, f"TEMP:UNIT CELS, (@{channels})")
    instrument_write(s, f"TEMP:ODET OFF, (@{channels})")
    instrument_write(s, f"TEMP:TC:RJUN:RSEL INT, (@{channels})")
    instrument_write(s, f"TEMP:TC:RJUN:SIM 28.5, (@{channels})")    
    instrument_write(s, f"TEMP:AZER ON, (@{channels})")
    instrument_write(s, f"TEMP:LINE:SYNC ON, (@{channels})")
    return


def CapacitorSetup(s,channels):
    # define the channel function
    instrument_write(s, f"FUNC 'CAP', (@{channels})")

    # set the capacitors range if needed
    # instrument_write(s, f"CAP:RANG 1, (@{channels})")
    return
