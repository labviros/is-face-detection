#!/bin/bash
set -e 

cd ../../

echo "|>>| Generating protobuf..."
docker run --rm -v $(pwd):$(pwd) -w $(pwd) luizcarloscf/docker-protobuf:master \
                                                        --python_out=./src/is_face_detector \
                                                        -I./src/conf/ options.proto
echo "|>>| Done!"