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


def main():

    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    op = load_options()
    face_detector = FaceDetector(op.model)
    re_topic = re.compile(r'CameraGateway.(\w+).Frame')

    broker_ok = re.match("amqp:\\/\\/([a-zA-Z0-9\\.]+)?", op.broker_uri)
    if not broker_ok:
        log.critical("Invalid broker uri \"{}\", expected amqp://<hostname>", op.broker_uri)

    channel = ServiceChannel(broker_ok.group(1))
    log.info('Connected to broker {}', broker_ok.group(1))

    zipkin_ok = re.match("http:\\/\\/([a-zA-Z0-9\\.]+)(:(\\d+))?", op.zipkin_uri)
    if not zipkin_ok:
        log.critical("Invalid zipkin uri \"{}\", expected http://<hostname>:<port>", op.zipkin_uri)

    exporter = ZipkinExporter(
        service_name=service_name,
        host_name=zipkin_ok.group(1),
        port=zipkin_ok.group(3),
        transport=AsyncTransport,
    )

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

        log.info(
            '{{detections: {:2d}, dropped_messages: {:2d}, took_ms: {{ detection: {:5.2f}, service: {:5.2f}}}}}',
            len(faces), dropped, span_duration_ms(detection_span), span_duration_ms(span))


if __name__ == "__main__":
    main()