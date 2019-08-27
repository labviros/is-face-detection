
# Face Detector Service

This service detect faces in images provided by the cameras.

## Streams

| Name | Input (topic/message) | Output (topic/message) | Description
| --- |--- | --- | --- |
|Face.Detection | **CameraGateway.\d+.Frame** [Image](https://github.com/labviros/is-msgs/blob/modern-cmake/docs/README.md#is.vision.Image) | **FaceDetector.\d+.Rendered** [Image](https://github.com/labviros/is-msgs/blob/modern-cmake/docs/README.md#is.vision.Image)|After detection, faces are drew on input image and published for visualization.
|Face.Detection| **CameraGateway.\d+.Frame** [Image](https://github.com/labviros/is-msgs/blob/modern-cmake/docs/README.md#is.vision.Image) | **FaceDetector.\d+.Detection** [Object Annotations](https://github.com/labviros/is-msgs/blob/modern-cmake/docs/README.md#is.vision.ObjectAnnotations) | Detect face on images published by cameras and publishes an ObjectAnnotations message containing all the face detected

## About
It is a machine learning based approach where a cascade function is trained and then used to detect objects in other images. [OpenCV](https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html) already contains many pre-trained classifiers for face, eyes, smiles, etc. 

You can choose the scale factor, minimal neighboors and minimal size.
## Developing

### is-wire-py

The repository [is-wire-py](https://github.com/labviros/is-wire-py) contains some examples about the pub/Sub middleware for the *is* architecture (python implementation).


### Protocols Buffer 
In case you need to make any change on options protobuf file, will be necessary to rebuild the documentation file and the python related to it. For do that, simply run the script [src/conf/generate_docs.sh].(https://github.com/labviros/is-face-detector/blob/master/src/conf/generate_docs.sh).
```shell
cd src/conf/
chmod +x generate_docs.sh
./generate_docs.sh
``` 
The service configuration is detailed below.

In case of any doubts about Protocol Buffers Objetcs, the [Protocol Buffer tutorials](https://developers.google.com/protocol-buffers/docs/pythontutorial) may help.
### Docker
The image docker used here support any application in python that uses [OpenCV](https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html). If you need another module, specify on [setup.py](https://github.com/labviros/is-face-detector/blob/master/setup.py). Maybe, your application will not run because the image docker doesn't contain some library. In this case, will be necessary edit the [etc/docker/Dockerfile](https://github.com/labviros/is-face-detector/blob/master/etc/docker/Dockerfile), by installing what do you need or using another base image. 

The repository [how-to](https://github.com/labviros/how-to/tree/master/deploy_an_app_to_k8s) contains a tutorial of deploying an application to a Kubernetes cluster. 

## Service Configuration

The options are set up in a [etc/conf/json](https://github.com/labviros/is-face-detector/blob/master/etc/conf/options.json) or passed by a configMap. The struct of the json file need to be like descript bellow, once the json file is converted into a protobuf object.

 <a name="top"/>

## Table of Contents

- [options.proto](#options.proto)
    - [FaceDetectorOptions](#.FaceDetectorOptions)
    - [HaarCascadeModel](#.HaarCascadeModel)
  
  
  
  




<a name="options.proto"/>
<p align="right"><a href="#top">Top</a></p>

## options.proto



<a name=".FaceDetectorOptions"/>

### FaceDetectorOptions
Service Configuration


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| broker_uri | [string](#string) |  |  |
| zipkin_host | [string](#string) |  |  |
| zipkin_port | [uint32](#uint32) |  |  |
| model | [HaarCascadeModel](#HaarCascadeModel) |  | Configurations of the HaarCascade model |






<a name=".HaarCascadeModel"/>

### HaarCascadeModel



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| model_file | [string](#string) |  | Path of the model |
| scale_factor | [float](#float) |  | The value indicates how much the image size is reduced at each image scale |
| min_neighbors | [uint32](#uint32) |  | How many “neighbors” each candidate rectangle should have |
| min_size | [google.protobuf.ListValue](#google.protobuf.ListValue) |  | The minimum object size |





 

 

 

 



