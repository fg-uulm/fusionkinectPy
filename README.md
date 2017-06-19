# fusionkinectPy
Python Library for FusionKit Kinect Access

# System Requirements
To use this library, you will need:
* a Kinect for XBox One, connected to
* a suitable PC running Windows 8 or higher
* having the Kinect SDK installed
* and running the FusionKit Server component

Please also make sure the PC is available via network (or use local networking / localhost/ 127.0.0.1).

# Features
The current version of this library allows to retrieve the following information from the Kinect camera via JS in real-time:
* Skeleton tracking data for up to 6 users
* IR marker tracking data (3D positions) for a (theoretically) unlimited number of markers
* Depth / point cloud data in full resolution as image or raw pixel array
* Thresholded 1-bit depth data as image or raw pixel array
* Blob data (size, 2D position) for objects exceeding the thresholds defined in the server software
* Audio stream, indicating direction and confidence for audio events
* RGB camera data (MJPEG stream - experimental)
* Facial features as delivered by the Kinect Face Recognition API (experimental) 

# Getting started
Please install openCV (> 3.0) and ws4py (> 0.4.2) before using this library.

See example.py for usage:

```python
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
```





