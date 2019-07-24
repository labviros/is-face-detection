#!/bin/bash
set -e 

if [ ! -f protoc-gen-doc ]; then
  wget "https://github.com/pseudomuto/protoc-gen-doc/releases/download/v1.1.0/protoc-gen-doc-1.1.0.linux-amd64.go1.10.tar.gz"
  tar xvf "protoc-gen-doc-1.1.0.linux-amd64.go1.10.tar.gz"
  rm "protoc-gen-doc-1.1.0.linux-amd64.go1.10.tar.gz"
  mv "protoc-gen-doc-1.1.0.linux-amd64.go1.10/protoc-gen-doc" .
  rmdir "protoc-gen-doc-1.1.0.linux-amd64.go1.10"
fi

protoc --plugin=protoc-gen-doc=./protoc-gen-doc --doc_out=. --doc_opt=markdown,README.md -I.. ../conf/*.proto
sed -i '/## Scalar Value Types/,$d' README.md 
mv README.md ../../
rm -rf protoc-gen-doc