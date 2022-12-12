#!/usr/bin/env python
PKG = 'collector'
import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import message_filters
import rosbag



class sub_and_pub():
    """ Class that synchronizes f/t sensor readings and image readings then
    publish to two separate nodes """
    def __init__(self):
        self.pub_img = rospy.Publisher('imgs_data', Float64, queue_size=10)
        self.pub_force = rospy.Publisher('force_data', WrenchStamped, queue_size=10)
        self.image_sub = message_filters.Subscriber("/magnitudes", Float64)
        self.info_sub = message_filters.Subscriber("/forque/forqueSensor", WrenchStamped)
        ts = message_filters.ApproximateTimeSynchronizer([self.image_sub, self.info_sub],10, 10, allow_headerless=True)
        ts.registerCallback(self.callback_sync)

    def callback_sync(self, img, w):
        self.pub_img.publish(img)
        self.pub_force.publish(w)



def listener():

    rospy.init_node('listener')
    a = sub_and_pub()
    rospy.spin()

if __name__ == '__main__':
    listener()
