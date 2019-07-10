import cv2



class FaceDetector:
    def __init__(self, op):
        self.options = op
        self.faceCascade = cv2.CascadeClassifier(op.model_file)
        self.min_neighbors = op.cascade_options.min_neighbors
        self.scale_factor = op.cascade_options.scale_factor

    def detect(self, image):
        # Read the image
        _image = image
        gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(image=gray, 
                                                       scaleFactor=self.scale_factor, 
                                                       minNeighbors=self.min_neighbors)
        return self.faces
    
