#!/usr/bin/env python
PKG = 'collector'
import roslib; roslib.load_manifest(PKG)
import rospy
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float64
from digit_interface.digit import Digit
from digit_interface.digit_handler import DigitHandler
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from opticalFlow import OpticalReader
from vectorField import VectorField
from digit.srv import Tare, TareResponse
import cv2
import numpy



def talker():
    pub = rospy.Publisher('floats', numpy_msg(Image),queue_size=10)
    magnitude_pub = rospy.Publisher("magnitudes", Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    s = rospy.Service('tare', Tare, handle_tare)
    print ("ready to tare")
    r = rospy.Rate(100) # 100hz
    digit = Digit("D20201")
    global is_tare
    is_tare = False
    init_img = None
    curr_img = None
    viz = True
    digit.connect()
    bridge = CvBridge()
    flow = OpticalReader()
    while not rospy.is_shutdown():

        a = digit.get_frame()
        vField = None

        if init_img is None or is_tare:
            init_img = a 
            is_tare = False
            print ("Tare successful")
        else:
            curr_img = a 
            vField = flow.computeOpticalFlow(init_img, curr_img, viz)

            magnitude_pub.publish(vField.get_magnitude())


        msg = bridge.cv2_to_imgmsg(a)
        msg.header.stamp = rospy.Time.now()
        pub.publish(msg)
        r.sleep()

def tare_server():
    rospy.init_node('tare_server')
    print ("Ready to tare")
    
    rospy.spin()

def handle_tare(req):
    global is_tare
    is_tare = True
    return TareResponse(True)




if __name__ == '__main__':
    
    talker()
    