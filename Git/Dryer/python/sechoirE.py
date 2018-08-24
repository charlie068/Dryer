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
import smbus
#import time
import subprocess
import RPi.GPIO as GPIO
import max31865

# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Import the MCP4725 module.
#import Adafruit_MCP4725

#email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders


   
        
   
   
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
    
  
	
		 
#### MAIN PROGRAM ##########################################################
if __name__ == "__main__":
	print("hello1")
	if len(sys.argv)>1:
		if sys.argv[1]=='delete':
			print('deleting')
			deletetable()
	else:
		initialise()
		readconf()
		#entrywin()
		#Repeat loop 
		rt = RepeatedTimer((float(interval)*60), Main) # it auto-starts, no need of rt.start()


	### END MAIN #################################################################







