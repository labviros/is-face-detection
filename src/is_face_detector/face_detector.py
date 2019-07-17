import cv2


class FaceDetector:

    def __init__(self, op):
        self.faceCascade = cv2.CascadeClassifier(op.model_file)
        self.min_neighbors = op.min_neighbors
        self.scale_factor = op.scale_factor
        self.min_size = tuple([int(v.number_value) for v in op.min_size.values])

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(
            image=gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size)
        return self.faces
