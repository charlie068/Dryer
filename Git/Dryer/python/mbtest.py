#!/usr/bin/env python3
#Stop variateur
import minimalmodbus
import serial
import time
def stopDAC():
 
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
        #minimal ModBUS
        instrument.serial.port          # this is the serial port name
        instrument.serial.baudrate = 19200   # Baud
        instrument.serial.bytesize = 8
        instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout  = 10   # seconds
        instrument.address=1     # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

 
        # Registernumber, number of decimals
        
        #instrument.write_register(8501, 0x0080, 0) # Registernumber, value, number of decimals for storage
        instrument.write_register(8501, 0x0006, 0) # Registernumber, value, number of decimals for storage


stopDAC()

    
