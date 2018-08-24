#!/usr/bin/env python3
"""
Created on Sat Jul 14 07:47:31 2018

@author: JeanCharles ISNER

IoT working on Rapsberry to regulate a Variator Schneider ATV312 in function of the humidity of Maize
Two humidity sensors are read via an ADC, an RTD temperature probe is read from a max31865.
The data are saved on a sql server and the average is taken to set the speed of the motor in Hz to regulate the time of drying. 
A website (PHP) is connected to the database and a jsGraph is used to produce javascript linegraph from the database.
The website allows to set the parameters of the drying program

"""
# -*- coding: utf-8 -*-
##### ALL imports ####################################################
## sondes haut = 3+4 ms1
## sondes bas = 1+2 (temp + Hum)


import sys
import threading 
import time
import configparser
import smtplib
import tkinter as Tk 
from datetime import datetime,timedelta
import os
import pymysql
import math
#import json
import minimalmodbus
import smbus2
#import time
import subprocess
import  math
import serial

import RPi.GPIO as GPIO
from max31865 import max31865

# Import the ADS1x15 module.
import Adafruit_ADS1x15

#email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders

#for Si7021 (temperature and humidity air)
import Si7021
import pigpio


class convert:
# sonde basse  12.5% = 5557 (ms2)
# 33.9% = 16000
#sonde haute 12.5 = 1900 (ms1)
#33.9 = 8500


    def ts1(value):
        return ((value-11340.766)/199.28) 
    def ms1(value):
        return float((value+1955)/308.4)
    def ts2(value):
        return ((value-8836.13)/265.58)
    def ms2(value):
        return float((value+543)/488)
    def perc_to_herz(value):
        return (1.233*value-7.757)
    
   
## Timer to repeat every 'interval' minute
class RepeatedTimer(object):
  def __init__(self, function, *args, **kwargs):
    self._timer = None
    #self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += (float(interval)*60)
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
    
## Timer to repeat every x secs
class RepeatedTimer2(object):
  def __init__(self, function, intervalb, *args, **kwargs):
    self._timer = None
    self.intervalb = intervalb
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.intervalb
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
    
class MyApp:
    """"""
    def __init__(self, parent): 
        """Constructor"""
        self.root = parent
        self.root.title("Sechoir Settings")
        self.root.geometry("250x300")
        self.frame = Tk.Frame(parent)
        self.frame.pack()
        
         #variables
        self.wSm = Tk.StringVar()
        self.woffset = Tk.StringVar()
        self.wfacta = Tk.StringVar()
        self.wfactb = Tk.StringVar()
        self.wminspeed = Tk.StringVar()
        self.wmaxspeed = Tk.StringVar()
        self.winterval = Tk.StringVar()
        self.wlimitmin = Tk.StringVar()
        self.wlimitmax = Tk.StringVar()
        
        
        self.var=Tk.IntVar()        
        
         #Label
        label_m=Tk.Label(self.frame, text="Set Moisture (%)", width=17, anchor="e")
        label_o=Tk.Label(self.frame, text="Offset", width=17, anchor="e")
        label_facta=Tk.Label(self.frame, text="Factor A",width=17, anchor="e")
        label_factb=Tk.Label(self.frame, text="Factor B", width=17,anchor="e")
        label_minmot=Tk.Label(self.frame, text="Min motor speed",width=17,anchor="e")
        label_manmot=Tk.Label(self.frame, text="Max motor speed", width=17,anchor="e")
        label_interval=Tk.Label(self.frame, text="Reading interval (min)", width=17,anchor="e")
        label_limitmin=Tk.Label(self.frame, text="Limit High (%)", width=17,anchor="e")
        label_limitmax=Tk.Label(self.frame, text="Limit Low (%)", width=17,anchor="e")
        
        label_chk=Tk.Label(self.frame, text="Erase Data", width=17, anchor="e")
         #grid labels
        label_m.grid(row=0)
        label_o.grid(row=1)
        label_facta.grid(row=2)
        label_factb.grid(row=3)
        label_minmot.grid(row=4)
        label_manmot.grid(row=5)
        label_interval.grid(row=6)
        label_limitmin.grid(row=7)
        label_limitmax.grid(row=8)
        label_chk.grid(row=9, sticky='W')
        
        

         #Entries
        entr_m = Tk.Entry(self.frame, width = 7, textvariable = self.wSm)
        entr_o = Tk.Entry(self.frame, width = 7, textvariable = self.woffset)
        entr_facta = Tk.Entry(self.frame, width = 7, textvariable = self.wfacta)
        entr_factb = Tk.Entry(self.frame, width = 7, textvariable = self.wfactb)
        entr_minmot = Tk.Entry(self.frame, width = 7, textvariable = self.wminspeed)
        entr_manmot = Tk.Entry(self.frame, width = 7, textvariable = self.wmaxspeed)
        entr_interval = Tk.Entry(self.frame, width = 7, textvariable = self.winterval)
        entr_limitmin = Tk.Entry(self.frame, width = 7, textvariable = self.wlimitmin)
        entr_limitmax = Tk.Entry(self.frame, width = 7, textvariable = self.wlimitmax)
        
        label_chk = Tk.Entry(self.frame, width = 7, textvariable = self.wminspeed)       
        
        
        
        
         #grid entries
        entr_m.grid(row=0, column=1)
        entr_o .grid(row=1, column=1)
        entr_facta.grid(row=2, column=1)
        entr_factb.grid(row=3, column=1)
        entr_minmot.grid(row=4, column=1)
        entr_manmot.grid(row=5, column=1)
        entr_interval.grid(row=6, column=1)
        entr_limitmin.grid(row=7, column=1) 
        entr_limitmax.grid(row=8, column=1)
        
         #Defaulf Values:
        entr_m.insert(10,Sm)
        entr_o.insert(10,offset) 
        entr_facta.insert(10,facta)
        entr_factb.insert(10,factb)
        entr_minmot.insert(10,minspeed)
        entr_manmot.insert(10,maxspeed)
        entr_interval.insert(10,interval)
        entr_limitmin.insert(10,limitmin) 
        entr_limitmax.insert(10,limitmax)
        
  
         #Checkbox
        Chk = Tk.Checkbutton(self.frame, text='', variable=self.var, width = 7, anchor="w")
        Chk.grid(row=9, column=1)
        
         #Button
        QuitButton = Tk.Button(self.frame, text="Discard Changes", command=self.quitter)
        QuitButton.grid(row=12, column=0)
        SaveButton = Tk.Button(self.frame, text='Save', command=self.getvariable)
        SaveButton.grid(row=12, column=1)
        
        
     #----------------------------------------------------------------------
    def getvariable(self):
        getvariable2(self.wSm.get(),self.woffset.get(),self.wfacta.get(),self.wfactb.get(),self.wminspeed.get(),self.wmaxspeed.get(),self.var.get(), self.winterval.get(), self.wlimitmin.get(), self.wlimitmax.get())
        self.root.destroy()

    def quitter(self):
        self.root.destroy()
        
def getvariable2(wSm, woffset, wfacta, wfactb, wminspeed, wmaxspeed, werasedata, winterval, wlimitmin, wlimitmax):
    global Sm,facta, factb,offset, minspeed, maxspeed,interval,limitmin, limitmax

    Sm=float(wSm)
    offset=float(woffset)
    facta=float(wfacta)
    factb=float(wfactb)
    minspeed=float(wminspeed)
    maxspeed=float(wmaxspeed)
    interval=float(winterval)
    limitmin=float(wlimitmin)
    limitmax=float(wlimitmax)
    writeconf()
    
    if (werasedata):
        print ("deleting data")
        deletetable()
        inidb()

def initialise():
    global dir_path,Ts1, Ms1, Ts2, Ms2, speedM, Ti, HuAir, \
            TAir, offset, facta, factb, maxspeed, minspeed,\
            Sm, db,cursor, interval, limitmin, limitmax, bus,\
            adc, adc2, GAIN, configfile, config, max31,\
            s, instrument, Tm, range_error

    
    #default values
    Ts1=0       #temperature sensor1
    Ms1=0       #moisture sensor1
    Ts2=0       #temperature sensor2
    Ms2=0       #moisture sensor2
    speedM=25   #speedmotor
    Ti=datetime.now()       #time
    Sm=15        #Set moisture
    HuAir=0     #Humidity air
    TAir=0      #temperature air
    interval=2
    limitmin = 17
    limitmax=13
    Tm=datetime.now() #time for emails
    range_error=False

    #Parameters:
    offset=0    #offset
    facta=0     #facteur of the formula a
    factb=0     #facteur of the formula b
    maxspeed=50
    minspeed=0

    #initialise db
    inidb()

    #intialise bus for temperature and humidity reading
    #bus = smbus2.SMBus(1)

    #intialise ADC
    adc = Adafruit_ADS1x15.ADS1115()
    adc = Adafruit_ADS1x15.ADS1115(address=0x4A, busnum=1)
    adc2 = Adafruit_ADS1x15.ADS1115()
    adc2 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    GAIN = 2/3
    
    #config file
    configfile="/var/www/html/configfolder/config.ini"
    config = configparser.ConfigParser()
    
    #Si7021:
    pi = pigpio.pi()
    s = Si7021.sensor(pi)  
    
    #minimalbus
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
    instrument.serial.port          # this is the serial port name
    instrument.serial.baudrate = 19200   # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 10   # seconds
    instrument.address=1     # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    #Set Registers
    instrument.write_register(8501, 0x0080, 0) #reset fault
    if record_only==True:
        print("Setting to Manual")
        instrument.write_register(8413, 0x0001, 0) #Manual set Fr1 to AI1
    elif record_only==False:
        print("Setting to Controlled")
        instrument.write_register(8413, 0x00A4, 0) #Automatic. set Fr1 to ModBus 
        instrument.write_register(8501, 0x0006, 0) # set it read to switch on
        instrument.write_register(8501, 0x0007, 0) # set it switch on
        instrument.write_register(8501, 0x000f, 0) # start
        instrument.write_register(8502, 0, 0) # put speed at 0Hz
    

def inidb():
    # Open database connection
    db = pymysql.connect("127.0.0.1","root","")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    #create database
    cursor.execute("""CREATE DATABASE IF NOT EXISTS Sechoirdb""")
    db.commit()
    #use database
    cursor.execute("""USE Sechoirdb""")
    db.commit()
    #create Data table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Data(
                    Time TIMESTAMP,
                    Ts1 FLOAT,
                    Ms1 FLOAT,
                    Ts2 FLOAT,
                    Ms2 FLOAT,
                    speedM FLOAT,
                    Sm FLOAT,
                    HuAir FLOAT,
                    TGrain FLOAT,
                    TAir FLOAT )""")
    
    db.commit()
    db.close()

#calculation
def calculate():  
    diff=Sm-Ms1 
    speedM=facta*Sm-factb*Ms1 
    factc= (facta) * (diff)
    speedM = (offset + 4095) / (1 + math.frexp(-factc))
    #print(speedM)   
    
    
###read value from configuration file ########################################
def readconf():
    global Sm,facta, factb,offset, minspeed, maxspeed, interval, limitmin, limitmax, integrtime
    if  os.path.exists(configfile):
        ##config = configparser.ConfigParser()
        config.read(configfile)
        Sm=float(config['DEFAULT']['Set Moisture %'])
        offset=float(config['DEFAULT']['Offset'])
        facta=float(config['DEFAULT']['Factor A'])
        factb=float(config['DEFAULT']['Factor B'])
        minspeed=float(config['DEFAULT']['Min motor speed'])
        maxspeed=float(config['DEFAULT']['Max motor speed'])
        interval=float(config['DEFAULT']['Reading Interval'])
        limitmin=float(config['DEFAULT']['Limit Alert Low'])
        limitmax=float(config['DEFAULT']['Limit Alert High'])
        integrtime=float(config['DEFAULT']['integration time'])


### 1st time Write value in configuration file ###############################
def writeconf():
    ##config = configparser.ConfigParser()
    config['DEFAULT']['Set Moisture %']=str(Sm)
    config['DEFAULT']['Offset']=str(offset)
    config['DEFAULT']['Factor A']=str(facta)
    config['DEFAULT']['Factor B']=str(factb)
    config['DEFAULT']['Min motor speed']=str(minspeed)
    config['DEFAULT']['Max motor speed']=str(maxspeed)
    config['DEFAULT']['Reading Interval']=str(interval)
    config['DEFAULT']['Limit Alert Low']=str(limitmin)
    config['DEFAULT']['Limit Alert High']=str(limitmax)


    with open(configfile, 'w') as cconfigfile:
        config.write(cconfigfile)

    subprocess.call(['chmod', '0777', configfile])
    

def wait():
    time.sleep(0.1)

def readADC():
    try:
        
        ## Read Value from max31865 -> RTD temperature value for TGrain
        max31 = max31865()
        TGrain=max31.readTemp()
        
        ##Read temperature and Humidity ################
        celsTemp=round(s.temperature(),2)
        humidity=round(s.humidity(),2)

        ## reading Value from ADC  ########################################
        # Read all the ADC channel values in a list.
        values = []
        for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
            values.append(adc.read_adc(i, gain=GAIN))
        
        values.extend([humidity,celsTemp,TGrain])
        # Read the specified ADC channel using the previously set gain value.
        values.append(adc2.read_adc(0, gain=GAIN))

        #debugging, print all crude values:
        print(values)
        
        return (values)
    except IOError:
        print("Failed to read from instrument ADC")
    
### WRITE in ModBUS   ########################################

def writeDAC(speedmotor):
        
        instrument.write_register(8502, speedmotor, 0) # put speed at speedmotor Hz

        
### Send email if of limits    ########################################
def sendmail(eMs2):

     
    fromaddr = "sechoir.rouffach@gmail.com"
    toaddr = "charlie068@gmail.com"    #destinataire
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Humidity Alert"
     
    body = str(eMs2)
     
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "sechoir10!")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
   

def writedataf(Ts1, Ms1, Ts2, Ms2, HuAir, TAir, TGrain, speedM):
    global Tm, range_error

    # Open database connection
    db = pymysql.connect("127.0.0.1","root","")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("""USE Sechoirdb""")
    db.commit()
    #command to insert all values in the db
    sql =       """INSERT INTO Data(Ts1,Ms1,Ts2,
                    Ms2,speedM,Sm,HuAir,TAir,TGrain)
                    VALUES ("""+str(Ts1)+","+str(Ms1)+","+str(Ts2)+","+str(Ms2)+","+str(speedM)+","+str(Sm)+","+str(HuAir)+","+str(TAir)+","+str(TGrain)+")"""
    
       # Execute the SQL command
    cursor.execute(sql)
       # Commit your changes in the database
    db.commit()
    #except:
       # Rollback in case there is any error
     #  db.rollback()
    
    # disconnect from server
    db.close() 
    
    
    #Test if of limits and send email and send an email not more than one every 10min
    
    #''' uncomment to activate email notification
    
    
    if (((Ms2)>float(limitmax)) or ((Ms2)<float(limitmin))):
        if ((datetime.now()-Tm).seconds)>600:  #600=10 minutes
            sendmail("Humidity is outside the setting range: "+str(Ms2)+"%")
            Tm=datetime.now()
            range_error=True
    elif ((Ms2<float(limitmax)) and (Ms2>float(limitmin)) and (range_error==True)):
        range_error=False
        sendmail("Humidity is back to normal and is now: "+str(Ms2)+"%")
        
    
    
def readdataf():  #make an average of last n minutes

    Ti=datetime.now()
    TiRange=(Ti-timedelta(hours=integrtime)) #can be made automatic in the future
    
   
          # Open database connection
    db = pymysql.connect("127.0.0.1","root","")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("""USE Sechoirdb""")

    sql = """SELECT AVG(Ts1),AVG(Ms1), AVG(Ts2), AVG(Ms2), AVG(HuAir), AVG(TAir), AVG(speedM), AVG(TGrain) FROM Data 
          WHERE Time BETWEEN '"""+str(TiRange)+"' AND '"+str(Ti)+"'""" 
    
    
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
  
    #take average
    aver_read={"Ts1": results[0][0],"Ms1": results[0][1], "Ts2": results[0][2],"Ms2": results[0][3],"speedM": results[0][6],"Tgrain": results[0][7]} 
    
    db.close()
    return ((aver_read))
    

        
def deletetable():
    db = pymysql.connect("127.0.0.1","root","")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("""USE Sechoirdb""")
    
    #delete table
    sql = "DROP TABLE Data"
    
    # Execute the SQL command
    cursor.execute(sql)
    
    
def entrywin():
    if __name__ == "__main__":
        root = Tk.Tk()
        root.geometry("800x600")
        MyApp(root)
        root.mainloop()

######## MAIN LOOP##################################################

def principal():
    global speedM
    try:
        registr= instrument.read_register(8502, 0)
        #read conf file values in case they were changed by website
        readconf()
        #read Values from ADC
        #1-->Entree / 2-->Exit
        readings=readADC()
        ts1=readings[2]
        ms1=readings[3]
        ts2=readings[0]
        ms2=readings[1]
        HumAir=readings[4]
        TAir=readings[5]
        ts1_conv=convert.ts1(ts1)
        ms1_conv=convert.ms1(ms1)
        ts2_conv=convert.ts2(ts2)
        ms2_conv=convert.ms2(ms2)
        TGrain=readings[6]
        
        #for debugging
        if (False):
            print ("Date: "+datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
            print ("Temperature 1: %.1f" % ts1)
            print ("Humidity 1: %.1f" % ms1)
            print ("Temperature 2: %.1f" % ts2)
            print ("Humidity 2: %.1f" % ms2)
            print("--")
            print ("Temperature 1: %.1fC"  %ts1_conv)
            print ("Humidity 1: %.1f%%" % ms1_conv)
            print ("Temperature 2: %.1fC" % ts2_conv)
            print ("Humidity 2: %.1f%%" % ms2_conv)
            print("--")
            print("Air Temperature : %.1fC" %TAir)
            print("Air Humidity : %.1f%%" %HumAir)
            print("--")
            print("Temperature Grain: %.1fC" %TGrain)
            print("--")
        
        

        #calculation
        eff_factor=float(1)

        #modify the speed of the motor according the error in the future
        #print("Efficiency Factor: "+str(eff_factor))
        #eff_factor=(ms2(t)-ms1(t-2h))/ms1(t-2h)
        #

        try:
            results_data=readdataf()
            ms1_av=float(results_data["Ms1"])
            #print("making average")
        except:
            ms1_av=ms1_conv
            #print("initialise ms1 average")
            
        #sigmoid curve, alternative to linear curve
        #speedM=(offset+(facta/(1+math.exp((factb*(ms1-Sm))))))*eff_factor
        #speedM=convert.perc_to_herz((-facta*(ms1-Sm)+factb))
    
        #define speed of motor according to the difference of ms1 and the factor entered drom the user
        #linear curve
        speedM_perc=(facta*(ms1_av-Sm+offset)+factb)
        speedM=convert.perc_to_herz(speedM_perc)
        
        #stay in the speedrange defined by the user
        if(speedM>maxspeed):
            speedM=maxspeed
        elif (speedM<minspeed):
            speedM=minspeed

        #write data in db
        writedataf(ts1_conv,\
                    ms1_conv,\
                    ts2_conv,\
                    ms2_conv,\
                    (HumAir),\
                    (TAir),\
                    (TGrain),\
                    (speedM))           


    except:
        print ("failed to read ADC")
        
    if (record_only==False):
        writeDAC(speedM)
        
        
def keepmb_alive():
    #modbus needs to send information at least every 30 seconds otherwise, it gets into error mode
    registr2 = instrument.read_register(3202, 0)
         
#### MAIN PROGRAM ##########################################################
print("hello")

global record_only
if __name__ == "__main__":
    temps_attente=0
    if len(sys.argv)>1:
        if sys.argv[1]=='delete':
            deletetable()
        elif sys.argv[1].isnumeric():
            if sys.argv[2]=='R':
                record_only=True
                print("Record date only")
            else:
                record_only=False
                print("raspberry controlling dryer")
            temps_attente=sys.argv[1]
            #initialise all values
            initialise()
            #read the configuration file
            readconf()
            #setting window on linux without website
            #entrywin()    
            print("Program Starting")
            #wait before start
            time.sleep(float(temps_attente)*60)
            
            #Repeat loop 
            #loop for main program
            rt = RepeatedTimer(principal) # it auto-starts, no need of rt.start()
            #loop for keeping modbus alive (every 10sec)
            rt2 = RepeatedTimer2(keepmb_alive,10)
            

### END MAIN #################################################################







