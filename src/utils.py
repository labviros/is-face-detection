import json
from is_wire.core import Logger
import argparse

def load_options():
    log = Logger(name='LoadOptions')
    parser = argparse.ArgumentParser('Load options for face detector!')
    parser.add_argument("-o", "--op", type=str, help="Load options")
    args = parser.parse_args()
    print (args)
    with open (args.op, 'r') as f:
        op = json.load(f)        
    return op
