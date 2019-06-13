import json
from is_wire.core import Logger
import argparse
import numpy as np
import cv2
from is_msgs.image_pb2 import Image, ObjectAnnotations, ObjectLabels

def load_options():
    log = Logger(name='LoadOptions')
    parser = argparse.ArgumentParser('Load options for face detector!')
    parser.add_argument("-o", "--op", type=str, help="Load options")
    args = parser.parse_args()
    with open (args.op, 'r') as f:
        op = json.load(f)        
    return op

def get_np_image(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image