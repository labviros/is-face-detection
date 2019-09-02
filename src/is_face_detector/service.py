import re
import dateutil.parser as dp

from is_wire.core import Logger, Channel, Subscription, Message
from is_wire.core import Tracer, AsyncTransport
from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from is_msgs.image_pb2 import Image

from .face_detector import FaceDetector
from .service_channel import ServiceChannel
from .image_tools import to_image, to_np, draw_detection
from .utils import load_options


def span_duration_ms(span):
    dt = dp.parse(span.end_time) - dp.parse(span.start_time)
    return dt.total_seconds() * 1000.0


def create_exporter(service_name, uri):
    log = Logger(name="CreateExporter")
    zipkin_ok = re.match("http:\\/\\/([a-zA-Z0-9\\.]+)(:(\\d+))?", uri)
    if not zipkin_ok:
        log.critical("Invalid zipkin uri \"{}\", expected http://<hostname>:<port>", uri)
    exporter = ZipkinExporter(
        service_name=service_name,
        host_name=zipkin_ok.group(1),
        port=zipkin_ok.group(3),
        transport=AsyncTransport)
    return exporter


def main():

    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    op = load_options()
    face_detector = FaceDetector(op.model)
    re_topic = re.compile(r'CameraGateway.(\w+).Frame')

    channel = ServiceChannel(op.broker_uri)
    log.info('Connected to broker {}', op.broker_uri)

    exporter = create_exporter(service_name=service_name, uri=op.zipkin_uri)

    subscription = Subscription(channel=channel, name=service_name)
    subscription.subscribe(topic='CameraGateway.*.Frame')

    while True:
        msg, dropped = channel.consume(return_dropped=True)

        tracer = Tracer(exporter, span_context=msg.extract_tracing())
        span = tracer.start_span(name='detection_and_render')
        detection_span = None

        with tracer.span(name='unpack'):
            im = msg.unpack(Image)
            im_np = to_np(im)

        with tracer.span(name='detection') as _span:
            faces = face_detector.detect(im_np)
            detection_span = _span

        with tracer.span(name='render_pack_publish'):
            img_rendered = draw_detection(im_np, faces)
            rendered_msg = Message()
            rendered_msg.topic = re_topic.sub(r'FaceDetector.\1.Rendered', msg.topic)
            rendered_msg.pack(to_image(img_rendered))
            channel.publish(rendered_msg)

        span.add_attribute('Detections', len(faces))
        tracer.end_span()

        info = {
            'detections': len(faces),
            'dropped_messages': dropped,
            'took_ms': {
                'detection': round(span_duration_ms(detection_span), 2),
                'service': round(span_duration_ms(span), 2)
            }
        }

        log.info('{}', str(info).replace("'", '"'))


if __name__ == "__main__":
    main()