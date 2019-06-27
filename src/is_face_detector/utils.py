from is_wire.core import Logger
from google.protobuf.json_format import Parse
from options_pb2 import FaceDetectorOptions
import sys

def load_options():
    log = Logger(name='LoadingOptions')
    op_file = sys.argv[1] if len(sys.argv) > 1 else 'options.json'
    with open (op_file, 'r') as f:
        op = Parse(f.read(), FaceDetectorOptions())   
    return op

