#!/bin/bash
set -e 

cd ../../

docker run --rm \
  -v $(pwd):/out \
  -v $(pwd)/src/conf:/protos \
  pseudomuto/protoc-gen-doc --doc_opt=markdown,README.md


sed -i '/## Scalar Value Types/,$d' README.md 
sed  -i "/Scalar Value Types/d" README.md

