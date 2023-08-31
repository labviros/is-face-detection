from typing import Tuple
import cv2
import numpy as np
from nptyping import NDArray, Int8, Float32, Shape

from is_msgs.image_pb2 import ObjectAnnotations, Image

from is_face_detector.conf.options_pb2 import Model

Width = int
Height = int
Channels = int


class FaceDetector:
    def __init__(self, options: Model) -> None:
        if options.gpu:
            self._backend_id = cv2.dnn.DNN_BACKEND_CUDA
            if options.f16:
                self._target_id = cv2.dnn.DNN_TARGET_CUDA_FP16
            else:
                self._target_id = cv2.dnn.DNN_TARGET_CUDA
        else:
            self._backend_id = cv2.dnn.DNN_BACKEND_OPENCV
            self._target_id = cv2.dnn.DNN_TARGET_CPU

        self._input_size = (options.input_size.width, options.input_size.height)
        self._model = cv2.FaceDetectorYN.create(
            model=options.path,
            config="",
            input_size=self._input_size,
            score_threshold=options.conf_threshold,
            nms_threshold=options.nms_threshold,
            top_k=options.top_k,
            backend_id=self._backend_id,
            target_id=self._target_id,
        )

    @staticmethod
    def to_np(image: Image) -> NDArray[Shape["*, *, 3"], Int8]:
        buffer = np.frombuffer(image.data, dtype=np.uint8)
        output = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
        return output

    @staticmethod
    def to_image(
        image: Image, encode_format: str = ".jpeg", compression_level: float = 0.8
    ) -> Image:
        if encode_format == ".jpeg":
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == ".png":
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=image, params=params)
        return Image(data=cimage[1].tobytes())

    @staticmethod
    def visualize(
        image: NDArray[Shape["*, *, 3"], Int8], annotations: ObjectAnnotations
    ) -> NDArray[Shape["*, *, 3"], Int8]:
        for obj in annotations.objects:
            x1 = int(obj.region.vertices[0].x)
            y1 = int(obj.region.vertices[0].y)
            x2 = int(obj.region.vertices[1].x)
            y2 = int(obj.region.vertices[1].y)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return image

    @staticmethod
    def to_object_annotations(
        results: NDArray[Shape["*, 15"], Float32],
        image_shape: Tuple[Height, Width, Channels],
    ) -> ObjectAnnotations:
        annotations = ObjectAnnotations()
        for det in results:
            bounding_box = det[0:4].astype(np.int32)
            item = annotations.objects.add()
            vertex_1 = item.region.vertices.add()
            vertex_1.x = bounding_box[0]
            vertex_1.y = bounding_box[1]
            vertex_2 = item.region.vertices.add()
            vertex_2.x = bounding_box[0] + bounding_box[2]
            vertex_2.y = bounding_box[1] + bounding_box[3]
            item.label = "human_face"
            item.score = det[-1]
        annotations.resolution.width = image_shape[1]
        annotations.resolution.height = image_shape[0]
        return annotations

    def detect(self, array: NDArray[Shape["*, *, 3"], Int8]) -> ObjectAnnotations:
        height, width, _ = array.shape
        self._model.setInputSize((width, height))
        faces = self._model.detect(image=array)
        faces = faces[1] if faces[1] is not None else np.array([])
        return self.to_object_annotations(faces, image_shape=array.shape)
