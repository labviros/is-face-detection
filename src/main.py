from utils import load_options, get_np_image

from is_wire.core import Logger, Channel, Subscription
from faceDetection import FaceDetector
from is_msgs.image_pb2 import Image
import cv2
import time
op = load_options()

k = FaceDetector(op)



# Connect to the broker
channel = Channel("amqp://guest:guest@10.10.2.1:30000")

# Subscribe to the desired topic(s)
subscription = Subscription(channel)
subscription.subscribe(topic='CameraGateway.1.Frame')
# ... subscription.subscribe(topic="Other.Topic")

while True:
    msg= channel.consume()
    im = msg.unpack(Image)
    im_np = get_np_image(im)
    
    k.detect(im_np)
    for (x, y, w, h) in k.faces:
        cv2.rectangle(im_np, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('frame',im_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  