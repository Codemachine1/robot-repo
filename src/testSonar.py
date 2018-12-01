import RPi.GPIO as GPIO
import threading
import math
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.IN)
GPIO.setup(26,GPIO.IN)
def get_ping_distance(pinNumber):
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


while True:
    print(get_ping_distance(26))
    print(get_ping_distance(20))

    time.sleep(2)
