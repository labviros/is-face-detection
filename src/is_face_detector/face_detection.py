import cv2



class FaceDetector:
    def __init__(self, op):
        self.options = op
        self.faceCascade = cv2.CascadeClassifier(op.model_file)
        self.min_neighbors = op.cascade_options.min_neighbors
        self.scale_factor = op.cascade_options.scale_factor

    def detect(self, image):
        # Read the image
        self.image = image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(image=gray, 
                                                       scaleFactor=self.scale_factor, 
                                                       minNeighbors=self.min_neighbors)

    def draw_detection(self, colors, line_width):
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.image,(x,y),(x+w,y+h), colors, line_width)

    @property
    def scale_factor(self):
        return self._scale_factor
    
    @scale_factor.setter
    def scale_factor(self, value):
        try:
            if self.options.cascade_options.HasField("scale_factor"):
                self._scale_factor = value
        except ValueError:
            self._scale_factor = 1.1

    @property
    def min_neighbors(self):
        return self._min_neighbors
        
    @min_neighbors.setter
    def min_neighbors(self, value):
        try:
            if self.options.cascade_options.HasField("min_neighbors"):
                self._min_neighbors = value
        except ValueError:
            self._min_neighbors= 2