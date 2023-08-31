import dateutil.parser as dp

from is_msgs.image_pb2 import Image
from is_wire.core import Logger, Subscription, Message, Tracer

from is_face_detector.detector import FaceDetector
from is_face_detector.stream_channel import StreamChannel
from is_face_detector.utils import load_options, create_exporter, get_topic_id


def span_duration_ms(span):
    dt = dp.parse(span.end_time) - dp.parse(span.start_time)
    return dt.total_seconds() * 1000.0


def main():
    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    options = load_options(log=log)
    face_detector = FaceDetector(options.model)

    channel = StreamChannel(options.broker_uri)
    log.info("Connected to broker {}", options.broker_uri)

    exporter = create_exporter(
        service_name=service_name,
        uri=options.zipkin_uri,
        log=log,
    )

    subscription = Subscription(channel=channel, name=service_name)
    subscription.subscribe(topic="CameraGateway.3.Frame")

    while True:
        msg, dropped = channel.consume_last(return_dropped=True)

        tracer = Tracer(exporter, span_context=msg.extract_tracing())
        span = tracer.start_span(name="detection_and_render")
        detection_span = None

        with tracer.span(name="unpack"):
            im = msg.unpack(Image)
            im_np = face_detector.to_np(im)

        with tracer.span(name="detection") as _span:
            camera_id = get_topic_id(msg.topic)
            faces = face_detector.detect(im_np)
            detection_span = _span

        with tracer.span(name="pack_and_publish_detections"):
            faces_msg = Message()
            faces_msg.topic = "FaceDetector.{}.Detection".format(camera_id)
            faces_msg.inject_tracing(span)
            faces_msg.pack(faces)
            channel.publish(faces_msg)

        with tracer.span(name="render_pack_publish"):
            img_rendered = face_detector.visualize(im_np, faces)
            rendered_msg = Message()
            rendered_msg.topic = "FaceDetector.{}.Rendered".format(camera_id)
            rendered_msg.pack(face_detector.to_image(img_rendered))
            channel.publish(rendered_msg)

        span.add_attribute("Detections", len(faces.objects))
        tracer.end_span()

        info = {
            "detections": len(faces.objects),
            "dropped_messages": dropped,
            "took_ms": {
                "detection": round(span_duration_ms(detection_span), 2),
                "service": round(span_duration_ms(span), 2),
            },
        }
        log.info("{}", str(info).replace("'", '"'))


if __name__ == "__main__":
    main()
