#!/usr/bin/env python

import tf
from robotdriver import robotbasedriver

import thread

import time
import rospy
import math
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
rospy.init_node('motordriver', anonymous=True)
robotdriver=robotbasedriver(0.000875)
scan_frequency=.3
ROBOT_WIDTH=.237

def publishscans():
#        rospy.loginfo("publising laserscans")
	scan_publisher=rospy.Publisher('/laser_scan',LaserScan,queue_size=30)
	scans=[]
	for sensor in [26,20]:
		scans.append(robotdriver.get_ping_distance(sensor))
#	print(scans)
	msg=LaserScan()
	msg.header.stamp=rospy.Time.now()
	msg.header.frame_id="laser_frame"
	msg.angle_min=-.79
	msg.angle_max=.79
	msg.angle_increment=.79
	msg.ranges=scans
	msg.time_increment=(1/scan_frequency)/3
	msg.range_min=.4
	msg.range_max=2
	scan_publisher.publish(msg)

def publishOdometry(position,velocity,heading):
 #   rospy.loginfo("PUBLISH ODOMETRY")
    odom_publish=rospy.Publisher('/odom',Odometry,queue_size=30)
    tfbroadcaster=tf.TransformBroadcaster()
    msg = Odometry()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = '/odom'
    msg.child_frame_id =  '/base_footprint'
    msg.pose.pose.position.x=position[0]
    msg.pose.pose.position.y=position[1]
    msg.pose.pose.position.z=0
    msg.twist.twist.linear.x=velocity[0]
    msg.twist.twist.linear.y=0
    msg.twist.twist.linear.z=0
    msg.twist.twist.angular.x=0
    msg.twist.twist.angular.y=0
    msg.twist.twist.angular.z=velocity[1]
    msg.pose.pose.orientation=Quaternion(heading,0,0,1)
    odom_publish.publish(msg)
    tfbroadcaster.sendTransform((position[0],position[1],0),(heading,0,0,1),msg.header.stamp,msg.header.frame_id,msg.child_frame_id)
rospy.loginfo("starting robot proxy")
x=0
y=0
heading=0
previoustime=0

while not rospy.is_shutdown():
#    rospy.loginfo("run loop")
    deltaposition=robotdriver.get_encoderDistances()
    x+=deltaposition[0]
    y+=deltaposition[1]
    heading+=deltaposition[2]
    distance=math.sqrt(deltaposition[0]**2+deltaposition[1]**2)
    newtime=time.clock()
    deltatime=newtime-previoustime
    publishOdometry([x,y],[(distance/deltatime),(deltaposition[2]/deltatime)],heading)
    previoustime=newtime
    publishscans()

