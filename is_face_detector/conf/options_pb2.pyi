from is_msgs import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class FaceDetectorOptions(_message.Message):
    __slots__ = ["broker_uri", "model", "zipkin_uri"]
    BROKER_URI_FIELD_NUMBER: ClassVar[int]
    MODEL_FIELD_NUMBER: ClassVar[int]
    ZIPKIN_URI_FIELD_NUMBER: ClassVar[int]
    broker_uri: str
    model: Model
    zipkin_uri: str
    def __init__(self, broker_uri: Optional[str] = ..., zipkin_uri: Optional[str] = ..., model: Optional[Union[Model, Mapping]] = ...) -> None: ...

class Model(_message.Message):
    __slots__ = ["conf_threshold", "f16", "gpu", "nms_threshold", "path", "top_k"]
    CONF_THRESHOLD_FIELD_NUMBER: ClassVar[int]
    F16_FIELD_NUMBER: ClassVar[int]
    GPU_FIELD_NUMBER: ClassVar[int]
    NMS_THRESHOLD_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    TOP_K_FIELD_NUMBER: ClassVar[int]
    conf_threshold: float
    f16: bool
    gpu: bool
    nms_threshold: float
    path: str
    top_k: int
    def __init__(self, path: Optional[str] = ..., conf_threshold: Optional[float] = ..., nms_threshold: Optional[float] = ..., top_k: Optional[int] = ..., gpu: bool = ..., f16: bool = ...) -> None: ...
