import os
import cv2

from is_msgs.image_pb2 import ObjectAnnotations
from .options_pb2 import HaarCascadeModel


class FaceDetector:
    def __init__(self, op):
        if not isinstance(op, HaarCascadeModel):
            raise Exception(
                'Invalid parameter on \'FaceDetector\' constructor: not a HaarCascadeModel type')
        self.faceCascade = cv2.CascadeClassifier()
        if not self.faceCascade.load(os.path.abspath(op.model_file)):
            raise Exception('Cannot load the model')
        self.min_neighbors = op.min_neighbors
        self.scale_factor = op.scale_factor
        self.min_size = tuple([int(v.number_value) for v in op.min_size.values])

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(image=gray,
                                                  scaleFactor=self.scale_factor,
                                                  minNeighbors=self.min_neighbors,
                                                  minSize=self.min_size)
        return self._to_object_annotations(faces=faces, image_shape=image.shape[:2])

    def _to_object_annotations(self, faces, image_shape):
        obs = ObjectAnnotations()
        for x, y, width, height in faces:
            ob = obs.objects.add()
            v1 = ob.region.vertices.add()
            v1.x = x
            v1.y = y
            v2 = ob.region.vertices.add()
            v2.x = x + width
            v2.y = y + height
            ob.label = "human_face"
        obs.resolution.width = image_shape[1]
        obs.resolution.height = image_shape[0]
        return obs
