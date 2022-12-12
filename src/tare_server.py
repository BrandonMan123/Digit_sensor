#!/usr/bin/env python

from __future__ import print_function

from digit.srv import  Tare, TareResponse
import rospy

def handle_tare(req):
    
    return TareResponse(True)

def tare_server():
    rospy.init_node('tare_server')
    s = rospy.Service('tare', Tare, handle_tare)
    print("Ready to tare.")
    rospy.spin()

if __name__ == "__main__":
    # tare_server()
    pass
