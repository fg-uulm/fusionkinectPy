
import numpy as np
import cv2
from KinectClient import KinectClient

# Connect to Kinect camera server
kinect = KinectClient('ws://192.168.178.25:81/', protocols=['http-only'])
kinect.connect()

# Main Loop
while(True):
    # request frames from the kinect - using multiple identifiers is possible 
    # possible frame types:
    # d - Depth image
    # c - Color image
    # t - Threshold image
    # s - Dict of skeletons
    # m - Dict of markers
    # b - Dict of Blobs
    # a - Dict of audio events
    # f - Dict of face properties
    kinect.requestMultiple('ts')

    # display cv2 images from kinect
    if(kinect.getDepthImage() is not None):
        cv2.imshow('color frame',kinect.getDepthImage())
    if(kinect.getColorImage() is not None):
        cv2.imshow('depth frame',kinect.getColorImage())
    if(kinect.getThresholdImage() is not None):
        cv2.imshow('threshold frame',kinect.getThresholdImage())

    # show skeleton data stream on console
    if(kinect.getSkeletonData() is not None):
        print kinect.getSkeletonData()
    
    # loop timing and keyboard exit handler
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release resources
kinect.close()
cv2.destroyAllWindows()