#!/usr/bin/env python
# PKG = 'collector'
# import roslib; roslib.load_manifest(PKG)
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
    tare_offset = 0
    while not rospy.is_shutdown():

        a = digit.get_frame()
        vField = None

        if is_tare:
            curr_img = a 
            vField = flow.computeOpticalFlow(init_img, curr_img, viz)
            tare_offset = vField.get_magnitude()
            is_tare = False
            print(f"tare offset: {tare_offset}")
            print ("Tare successful")

        if init_img is None:
            init_img = a 
        else:
            curr_img = a 
            vField = flow.computeOpticalFlow(init_img, curr_img, viz)
            # print(f"magnitude: {vField.get_magnitude() }")
            magnitude_pub.publish(vField.get_magnitude()-tare_offset)


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
    