#!/usr/bin/env python3
"""
Created on Sat Jul 14 07:47:31 2018

@author: JeanCharles
"""
# -*- coding: utf-8 -*-
##### ALL imports ####################################################



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
import RPi.GPIO as GPIO
from max31865 import max31865

# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Import the MCP4725 module.
#import Adafruit_MCP4725

#email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders




class convert:
	def ts1(value):
		return ((value-11340.766)/199.28) 
	def ms1(value):
		return float(value/25767*100)
	def ts2(value):
		return ((value-8836.13)/265.58)
	def ms2(value):
		return (value/26672*100)
	def perc_to_herz(value):
		return (1.233*value-7.757)
	
   
        
   
   
## Timer to repeat every minute
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
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
      self.next_call += self.interval
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
			adc, GAIN, configfile, config, max31

	
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

	#Parameters:
	offset=0    #offset
	facta=0     #facteur of the formula a
	factb=0     #facteur of the formula b
	maxspeed=50
	minspeed=0
	#print ("3 ")

	#initialise db
	inidb()
	#print ("4 ")

	#intialise bus for temperature and humidity reading
	bus = smbus2.SMBus(1)
	#print ("5 ")

	#intialise ADC
	adc = Adafruit_ADS1x15.ADS1115()
	adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
	GAIN = 2/3
	#print (" 6")
	
	#initialise MAX31865
	#max31 = max31865()
	#print ("6.2")
	#config file
	configfile="/var/www/html/configfolder/config.ini"
	#print ("6.5")
	config = configparser.ConfigParser()
	#print (" 7")

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
    global Sm,facta, factb,offset, minspeed, maxspeed, interval, limitmin, limitmax
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
		#print("READ ADC")
		### Read VAlue from max31865 -> RTD temperature value for TGrain
		max31 = max31865()
		TGrain=max31.readTemp()
		#print("READ ADC2")
		#print(TGrain)
		#GPIO.cleanup()
		
		### Read temperature and Humidity ################
		
		## Get I2C bus
		bus.write_byte(0x40, 0xF5)
		 
		wait()
		 
		# SI7021 address, 0x40  Read 2 bytes, Humidity
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		 
		# Convert the data
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		 
		wait()
		bus.write_byte(0x40, 0xF3)
		wait()
		 
		# SI7021 address, 0x40 Read data 2 bytes, Temperature
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		 
		# Convert the data and output it
		celsTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85


		### reading Value from ADC  ########################################


		# Read all the ADC channel values in a list.
		values = []
	
		for i in range(4):
		# Read the specified ADC channel using the previously set gain value.
			values.append(adc.read_adc(i, gain=GAIN))
		
		values.extend([humidity,celsTemp,TGrain])
		#print(values)
		return (values)
	except IOError:
		print("Failed to read from instrument ADC")
		

    

    
### WRITE in ModBUS   ########################################

def writeDAC(speedmotor):
	try:
 
		#minimal ModBUS
		instrument.serial.port          # this is the serial port name
		instrument.serial.baudrate = 19200   # Baud
		instrument.serial.bytesize = 8
		instrument.serial.parity   = serial.PARITY_NONE
		instrument.serial.stopbits = 1
		instrument.serial.timeout  = 0.05   # seconds

		instrument.address=1     # this is the slave address number
		instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

		instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)

		## Read temperature (PV = ProcessValue) ##
		#temperature = instrument.read_register(289, 1) # Registernumber, number of decimals
		#print temperature

		## Change Frequency ##
		speedmotor=(speedmotor*32676)/600
		instrument.write_register(3202, speedmotor, 1) # Registernumber, value, number of decimals for storage
		
	except IOError:
		print("Failed to read from instrument DAC")
		
		
### Send email if of limits    ########################################
def sendmail(eMs2):

     
    fromaddr = "sechoir.rouffach@gmail.com"
    toaddr = "charlie068@gmail.com"    #destinataire
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Humidity Alert"
     
    body = "Last reading Humidity is "+str(eMs2)
     
    msg.attach(MIMEText(body, 'plain'))
     
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "sechoir10!")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
   

def writedataf(Ts1, Ms1, Ts2, Ms2, HuAir, TAir, TGrain, speedM):
	#global Ts1, Ms1, Ts2, Ms2, HuAir, TAir
    # Open database connection
	#print("db opened1")
	db = pymysql.connect("127.0.0.1","root","")
    # prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor.execute("""USE Sechoirdb""")
	db.commit()
	#print("db opened2")
    #Ti=datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
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
	
	
	#Test if of limits and send email
	#if (((Ms2)>float(limitmax)) or ((Ms2)<float(limitmin))):sendmail(Ms2)	
    
def readdataf():  #make an average of last n minutes

    Ti=datetime.now()
    TiRange=(Ti-timedelta(hours=3))
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
    #print(results[0])
    aver_read={"Ts1": results[0][0],"Ms1": results[0][1], "Ts2": results[0][2],"Ms2": results[0][3],"speedM": results[0][6],"Tgrain": results[0][7]} 
    #print ("reading")
    #print (aver_read["Ts1"])
    
    db.close()
    return ((aver_read))
    

        
def deletetable():
    db = pymysql.connect("127.0.0.1","root","")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("""USE Sechoirdb""")

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
	#print("main")
	#readconf()
	#print("main2")
	global speedM
	try:
		#read conf file values in case they were changed by website
		readconf()
		#read Values from ADC
		readings=readADC()
		ts1=readings[0]
		ms1=readings[1]
		ts2=readings[2]
		ms2=readings[3]
		HumAir=readings[4]
		TAir=readings[5]
		ts1_conv=convert.ts1(ts1)
		ms1_conv=convert.ms1(ms1)
		ts2_conv=convert.ts2(ts2)
		ms2_conv=convert.ms2(ms2)
		TGrain=readings[6]
		#print ("ADC3")
		#print (TGrain)
		#print("main3")




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
		#sigmoid curve
		#speedM=(offset+(facta/(1+math.exp((factb*(ms1-Sm))))))*eff_factor
		#speedM=convert.perc_to_herz((-facta*(ms1-Sm)+factb))
	
		#linear curve
		speedM_perc=(facta*(ms1_av-Sm+offset)+factb)
		speedM=convert.perc_to_herz(speedM_perc)

		if(speedM>maxspeed):
			speedM=maxspeed
		elif (speedM<minspeed):
			speedM=minspeed
		#print ("Humidity Average: %.1f%% " % ms1_av)
		#print ("Vitesse Motor: %.1fHz " % speedM)
		#print ("Vitesse Motor: %.1f%%" % speedM_perc)

		#print("-----------------")
		
		#print ("Write data in db")
		writedataf(ts1_conv,\
					ms1_conv,\
					ts2_conv,\
					ms2_conv,\
					(HumAir),\
					(TAir),\
					(TGrain),\
					(speedM))			
		
		#writeDAC(speedM)
	


	except:
		print ("failed to read ADC")
		
		 
#### MAIN PROGRAM ##########################################################


if __name__ == "__main__":
	temps_attente=0
	if len(sys.argv)>1:
		if sys.argv[1]=='delete':
			#print('deleting')
			deletetable()
		elif sys.argv[1].isnumeric():
			temps_attente=sys.argv[1]
			initialise()
			readconf()
			#entrywin()
			#Repeat loop 
			#print("A")
			time.sleep(float(temps_attente)*60)
			#print("B")
			rt = RepeatedTimer((float(interval)*60), principal) # it auto-starts, no need of rt.start()

	### END MAIN #################################################################







