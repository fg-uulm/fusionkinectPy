'''
FusionKit Kinect Python Client
==============================
Allows access to Kinect (v2) data streams via Websocket when used with FusionKit

Prerequisites
- Running FusionKit SensorServer Instance, reachable over network
- Working Python environment with OpenCV (>= 3.0) and ws4py (>= 0.4.2) installed

Current Release Date: 18/06/2017
Current Release Version: 0.11 

Author: fg
'''

import numpy as np
import cv2
from ws4py.client.threadedclient import WebSocketClient
import json

# Kinect Class
class KinectClient(WebSocketClient):
    __lastmessage = None

    __skeletonData = None
    __markerData = None
    __blobData = None
    __thresholdDataAsImage = None
    __depthDataAsImage = None
    __colorDataAsImage = None
    __audioData = None
    __faceData = None

    def opened(self):        
        print "Connected to Kinect at "+self.url

    def closed(self, code, reason):
        print(("Closed down Kinect connection: ", code, reason))

    def received_message(self, m):
        try:
            self.__lastmessage = json.loads(str(m))
        except:
            print("Decoding error")
        
        if(self.__lastmessage['type'] == 32):
            self.__skeletonData = self.__lastmessage['Skeletons']
        elif(self.__lastmessage['type'] == 4):
            self.__markerData = self.__lastmessage['Markers']
        elif(self.__lastmessage['type'] == 1024):
            self.__blobData = self.__lastmessage['Blobs']
        elif(self.__lastmessage['type'] == 768):
            #print self.__lastmessage
            nparr = np.fromstring(self.__lastmessage['Frame'].decode('base64'), np.uint8)
            self.__thresholdDataAsImage = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        elif(self.__lastmessage['type'] == 8):
            nparr = np.fromstring(self.__lastmessage['Frame'].decode('base64'), np.uint8)
            self.__depthDataAsImage = cv2.imdecode(nparr,0)
        elif(self.__lastmessage['type'] == 128):
            nparr = np.fromstring(self.__lastmessage['Frame'].decode('base64'), np.uint8)
            self.__colorDataAsImage = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        elif(self.__lastmessage['type'] == 64):
            self.__audioData = self.__lastmessage['Frame']
        elif(self.__lastmessage['type'] == 1280):
            self.__faceData = json.loads(self.__lastmessage['Data']);

    def requestMultiple(self, requestWhat):
        #self.send(u'c')
        for channel in requestWhat:
            self.send(channel)

    def getDepthImage(self):
        return self.__depthDataAsImage

    def getColorImage(self):        
        return self.__colorDataAsImage        

    def getThresholdImage(self):
        return self.__thresholdDataAsImage

    def getSkeletonData(self):
        return self.__skeletonData

    def getAudioData(self):
        return self.__audioData

    def getFaceData(self):
        return self.__faceData

    def getMarkerData(self):
        return self.__markerData

    def getBlobData(self):
        return self.__blobData