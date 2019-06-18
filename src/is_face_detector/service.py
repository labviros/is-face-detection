from utils import load_options
from is_wire.core import Logger, Channel, Subscription, Message
from face_detection import FaceDetector
from is_msgs.image_pb2 import Image
import cv2
import time
import re
from options_pb2 import FaceDetectorOptions 
import image_tools as img

def main():

    service_name = "FaceDetector.Detection"
    log = Logger(name=service_name)
    op = load_options()
    face_detector = FaceDetector(op)
    re_topic = re.compile(r'CameraGateway.(\w+).Frame')
    channel = Channel(op.broker_uri)
    subscription = Subscription(channel=channel, name=service_name)
    subscription.subscribe(topic='CameraGateway.*.Frame')


    while True:
        msg= channel.consume()
        im = msg.unpack(Image)
        im_np = img.to_np(im)

        face_detector.detect(im_np)
        face_detector.draw_detection(colors=(0,255,0), line_width=1)
        
        log.info(str(len(face_detector.faces)))
        face_msgs = Message ()
        face_msgs.pack(img.to_image(face_detector.image))
        channel.publish(face_msgs, re_topic.sub(r'FaceDetector.\1.Rendered', msg.topic))

if __name__ == "__main__":
    main()