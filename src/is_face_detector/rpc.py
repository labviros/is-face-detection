from is_msgs.image_pb2 import Image, ObjectAnnotations
from is_wire.core import Channel, Logger, Status, StatusCode
from is_wire.rpc import ServiceProvider, LogInterceptor, TracingInterceptor

from .image_tools import to_np
from .face_detector import FaceDetector
from .utils import load_options, create_exporter


class RPCFaceDetector(FaceDetector):
    def __init__(self, options):
        super().__init__(options)

    def detect(self, image, ctx):
        try:
            return super().detect(to_np(image))
        except:
            return Status(code=StatusCode.INTERNAL_ERROR)


def main():
    service_name = 'FaceDetector.Detect'
    log = Logger(name=service_name)

    op = load_options()
    detector = RPCFaceDetector(op.model)

    channel = Channel(op.broker_uri)
    log.info('Connected to broker {}', op.broker_uri)

    provider = ServiceProvider(channel)
    provider.add_interceptor(LogInterceptor())

    exporter = create_exporter(service_name=service_name, uri=op.zipkin_uri)
    tracing = TracingInterceptor(exporter=exporter)
    provider.add_interceptor(tracing)

    provider.delegate(topic='FaceDetector.Detect',
                      function=detector.detect,
                      request_type=Image,
                      reply_type=ObjectAnnotations)

    provider.run()


if __name__ == "__main__":
    main()
