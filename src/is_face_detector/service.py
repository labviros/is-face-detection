from .utils import load_options
from is_wire.core import Logger, Channel, Subscription, Message
from .face_detector import FaceDetector
from is_msgs.image_pb2 import Image
import re
from .image_tools import to_image, to_np, draw_detection


def main():

    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    op = load_options()
    face_detector = FaceDetector(op.model)
    re_topic = re.compile(r'CameraGateway.(\w+).Frame')
    channel = Channel(op.broker_uri)
    subscription = Subscription(channel=channel, name=service_name)
    subscription.subscribe(topic='CameraGateway.*.Frame')

    while True:
        msg = channel.consume()

        #unpack
        im = msg.unpack(Image)
        im_np = to_np(im)

        #detections
        faces = face_detector.detect(im_np)

        #rendered
        img_rendered = draw_detection(im_np, faces)

        #pack and publish
        face_msgs = Message()
        face_msgs.pack(to_image(img_rendered))
        channel.publish(face_msgs, re_topic.sub(r'FaceDetector.\1.Rendered', msg.topic))


if __name__ == "__main__":
    main()