#!/usr/bin/env python
PKG = 'collector'
import roslib; roslib.load_manifest(PKG)
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import Float64MultiArray
from digit_interface.digit import Digit
from digit_interface.digit_handler import DigitHandler
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2


def callback(data):
    print (data.data)
    #cv2.imshow('',data.data)


def disp_img():

    rospy.init_node('visualizer', anonymous=True)
    rospy.Subscriber('floats', numpy_msg(Image), callback)

    rospy.spin()

if __name__ == "__main__":
    disp_img()