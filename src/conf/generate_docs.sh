#!/bin/bash
set -e 

cd ../../

echo "Generating documentation..."
docker run --rm \
  -v $(pwd):/out \
  -v $(pwd)/src/conf:/protos \
  pseudomuto/protoc-gen-doc --doc_opt=markdown,docs.md

sed -i '/## Scalar Value Types/,$d' docs.md 
sed  -i "/Scalar Value Types/d" docs.md

FILE=README.md
if [ -f "$FILE" ]; then
    echo "$FILE exist"
    sed -i '/# Protocol Documentation/,$d' README.md
else
    echo "$FILE does not exist, creating..."
    touch README.md
fi

 

cat docs.md >> README.md

rm docs.md
echo "Successfully generated documentation"

