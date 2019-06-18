from is_wire.core import Logger
from is_msgs.image_pb2 import Image, ObjectAnnotations
import numpy as np
import cv2



class FaceDetector:
    def __init__(self, op):
        self.faceCascade = cv2.CascadeClassifier(op.model_file)
        self.options = op
    def detect(self, image):
        # Read the image
        self.image = image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(image=gray, 
                                                       scaleFactor=self.options.cascade_options.scale_factor, 
                                                       minNeighbors=self.options.cascade_options.min_neighbors)

    def draw_detection(self, colors, line_width):
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.image,(x,y),(x+w,y+h), colors, line_width)

#imagePath = "/home/luiz/Desktop/is-face-detection/src/hodor.jpg"
