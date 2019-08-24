#!/bin/bash
set -e 

cd ../../

echo "Generating documentation..."
docker run --rm -v $(pwd):$(pwd) -w $(pwd) luizcarloscf/docker-protobuf:master \
                                                        --python_out=./src/is_face_detector \
                                                        --doc_out=. \
                                                        --doc_opt=markdown,docs.md \
                                                        -I./src/conf/ options.proto

sed -i '/## Scalar Value Types/,$d' docs.md 
sed  -i "/Scalar Value Types/d" docs.md
sed -i "/Protocol Documentation/d" docs.md

FILE=README.md
if [ -f "$FILE" ]; then
    echo "$FILE exist"
else
    echo "$FILE does not exist, creating..."
    touch README.md
fi


cat docs.md >> README.md

rm docs.md
echo "Successfully generated documentation"

