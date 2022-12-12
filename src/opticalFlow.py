import numpy as np
import cv2 as cv
from vectorField import VectorField


class OpticalReader():
    """
    Class for taking DIGIT sensor readings and converting them into an optical flow field
    """
    def __init__(self):
        # params for ShiTomasi corner detection
        max_corners = 100
        self.feature_params = dict( maxCorners = max_corners,
                            qualityLevel = 0.01,
                            minDistance = 5,
                            blockSize = 7 )
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15, 15),
                        maxLevel = 2,
                        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        self.color = np.random.randint(0, 255, (max_corners, 3))

    def computeOpticalFlow(self, img1, img2, viz=False):
        """ Compute optical flow between two images. Returns list of vectors.
        Code taken from 
        https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html"""
        
        old_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **(self.feature_params))
        # Create a mask image for drawing purposes
        mask = np.zeros_like(img1)
        frame_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        # calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **(self.lk_params))
        # Select good points
        if p1 is not None:
            good_new = p1[st==1]
            good_old = p0[st==1]

        # draw the tracks
        vecs = []
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            #get displacement vector
            displacement = np.array([a-c, b-d])
            vecs.append(displacement)
            if viz:
                mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), self.color[i].tolist(), 2)
                img2 = cv.circle(img2, (int(a), int(b)), 5, self.color[i].tolist(), -1)
        
        if viz:
            img = cv.add(img2, mask)
            cv.imshow('frame', img)
            cv.waitKey(1)
        
        return VectorField(vecs)
    
