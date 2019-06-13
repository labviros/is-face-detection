from utils import load_options, get_np_image, get_pb_image
from is_wire.core import Logger, Channel, Subscription, Message
from faceDetection import FaceDetector
from is_msgs.image_pb2 import Image
import cv2
import time
import re
from options_pb2 import FaceDetectorOptions 

def main():

    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    op = load_options()
    k = FaceDetector()
    re_topic = re.compile(r'CameraGateway.(\w+).Frame')
    channel = Channel(op.broker_uri)
    subscription = Subscription(channel=channel, name=service_name)
    subscription.subscribe(topic='CameraGateway.*.Frame')


    while True:
        msg= channel.consume()
        im = msg.unpack(Image)
        im_np = get_np_image(im)
        k.detect(im_np)
        for (x, y, w, h) in k.faces:
            cv2.rectangle(im_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
        log.info(str(len(k.faces)))
        face_msgs = Message ()
        face_msgs.pack(get_pb_image(im_np))
        channel.publish(face_msgs, re_topic.sub(r'FaceDetector.\1.Rendered', msg.topic))

if __name__ == "__main__":
    main()