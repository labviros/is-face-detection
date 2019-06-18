import json
from is_wire.core import Logger
import numpy as np
import cv2
from is_msgs.image_pb2 import Image, ObjectAnnotations, ObjectLabels
from google.protobuf.json_format import Parse
from options_pb2 import FaceDetectorOptions
import sys

def load_options():
    log = Logger(name='LoadingOptions')
    op_file = sys.argv[1] if len(sys.argv) > 1 else 'options.json'
    with open (op_file, 'r') as f:
        op = Parse(f.read(), FaceDetectorOptions())   
    return op

