#!/usr/bin/env python3

      
      
if __name__ == "__main__":

   import time
   import Si7021
   import pigpio
   import RPi.GPIO as GPIO
   
   pi = pigpio.pi()

   if not pi.connected:
      exit(0)

   s = Si7021.sensor(pi)  
   stop = time.time() + 10

   print("revision={:x} id1={:08x} id2={:08x}".format(s.firmware_revision(),
      s.electronic_id_1(), s.electronic_id_2()))

   while time.time() < stop:

      # print("{:.2f} {:.2f}".format(s.temperature(), s.humidity()))
      print(s.temperature())
      print(s.humidity())
      time.sleep(1)
	
	

   s.cancel()

   pi.stop()
   
   
   
   
