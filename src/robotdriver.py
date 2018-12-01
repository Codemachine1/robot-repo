#!/usr/bin/env python
from rrb3 import *
import RPi.GPIO as GPIO
import threading
import math
class robotbasedriver:

	def __init__(self,encoderDistance):
		self.rr = RRB3(9, 6)
		self.heading=0
		self.leftled=False
		self.rightled=False
		self.previousRightEncoderTicks=0
		self.previousLeftEncoderTicks=0
		self.encoderDistance=encoderDistance
		self.leftTicks=0
		self.rightTicks=0
		self.previoustime=0
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(19,GPIO.IN)
		GPIO.setup(16,GPIO.IN)
		def leftcallback(channel):
        		self.leftTicks+=1 
		def rightcallback(channel):
        		self.rightTicks+=1

		GPIO.add_event_detect(19, GPIO.FALLING, callback=leftcallback, bouncetime=1)
		GPIO.add_event_detect(16, GPIO.FALLING, callback=rightcallback, bouncetime=1)
	def toggle_left_led(self):
		if self.leftled:
			self.rr.set_led1(0)
			self.leftled=False
		else:
			self.rr.set_led1(1)
			self.leftled=True
	def toggle_right_led(self):
		if self.rightled:
			self.rr.set_led2(0)
			self.rightled=False
		else:
			self.rr.set_led2(1)
			self.rightled=True

	def get_ping_distance(self,pinNumber):
        	endtime=0
        	starttime=0
        	GPIO.setup(pinNumber, GPIO.OUT)
        	GPIO.output(pinNumber, 0)
        	time.sleep(0.000002) 
        	GPIO.output(pinNumber, 1)
        	time.sleep(0.000005)
	        GPIO.output(pinNumber, 0)
	        GPIO.setup(pinNumber, GPIO.IN)
	        while GPIO.input(pinNumber)==0:
	                starttime=time.time()
        	while GPIO.input(pinNumber)==1:
                	endtime=time.time()
	        duration=endtime-starttime  
        	distance=duration*34000/2
        	return distance
	def get_encoderDistances(self):
		drighttdistance=(self.encoderDistance*(self.leftTicks-self.previousLeftEncoderTicks))
		dleftdistance=((self.rightTicks-self.previousRightEncoderTicks)*self.encoderDistance)
		ds=(drighttdistance+dleftdistance)/2
    		dth=(drighttdistance-dleftdistance)/.237
		dx=ds*math.cos(self.heading+dth/2)
		dy=ds*math.sin(self.heading+dth/2)
		return (dx,dy,dth)

	def set_motor(self,leftMotorSpeed,rightMotorSpeed):
		if leftMotorSpeed<0:
			leftmotordirection=0
    		else:
        		leftmotordirection=1
    			rightmotordirection=0
    		if rightMotorSpeed<0:
        		rightmotordirection=0
    		else:
        		rightmotordirection=1

#		print("rightspeed:"+str(rightMotorSpeed)+"leftspeed:"+str(leftMotorSpeed))
		self.rr.set_motors(abs(leftMotorSpeed),leftmotordirection,abs(rightMotorSpeed),rightmotordirection)

