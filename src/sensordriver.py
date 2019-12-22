#!/usr/bin/env python

import tf
from robotdriver import robotbasedriver

import thread
CZDMtwp2E50CH6j0+bKPsPxG5QO65Yl82q7j7XP9
import time
import rospy
import math
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
rospy.init_node('sensordriver', anonymous=True)
robotdriver=robotbasedriver(0.000875)
scan_frequency=.3
ROBOT_WIDTH=.237

def callback(data):
    rospy.loginfo("motorData Received")
    rightMotorSpeed=0
    leftMotorSpeed=0
    leftMotorSpeed=data.linear.x-data.angular.z*ROBOT_WIDTH/2
    rightMotorSpeed= data.linear.x + data.angular.z*ROBOT_WIDTH/2
    rospy.loginfo("speed right:"+str(rightMotorSpeed)+" left motor speed"+str(leftMotorSpeed))

    robotdriver.set_motor(leftMotorSpeed,rightMotorSpeed)

rospy.loginfo("starting robot proxy")
rospy.Subscriber("cmd_vel",Twist,callback)
rospy.spin()
CZDMtwp2E50CH6j0+bKPsPxG5QO65Yl82q7j7XP9
