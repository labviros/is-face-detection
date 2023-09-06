import cv2
import socket

from is_msgs.image_pb2 import ObjectAnnotations
from is_wire.core import Channel, Message, Subscription
from is_face_detector.detector import FaceDetector



def main():
    image = cv2.imread("../etc/images/face.png")
    channel = Channel("amqp://guest:guest@10.20.5.2:30000")
    subscription = Subscription(channel)
    request = Message(
        content=FaceDetector.to_image(image=image),
        reply_to=subscription,
    )
    channel.publish(request, topic="FaceDetector.Detect")
    try:
        reply = channel.consume(timeout=5.0)
        response = reply.unpack(ObjectAnnotations)
        print('RPC Status:', reply.status, '\nResponse:', response)
    except socket.timeout:
        print('No reply :(')


if __name__ == "__main__":
    main()