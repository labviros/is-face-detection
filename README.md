# Face Detector Service

[![Docker image tag](https://img.shields.io/docker/v/labvisio/is-face-detector?sort=semver&style=flat-square)](https://hub.docker.com/r/labvisio/is-face-detector/tags)
[![Docker image size](https://img.shields.io/docker/image-size/labvisio/is-face-detector?sort=semver&style=flat-square)](https://hub.docker.com/r/labvisio/is-face-detector)
[![Docker pulls](https://img.shields.io/docker/pulls/labvisio/is-face-detector?style=flat-square)](https://hub.docker.com/r/labvisio/is-face-detector)

![Example Image](https://raw.githubusercontent.com/labvisio/is-face-detector/master/etc/images/face.png)


In a simplified manner, a service within the Intelligent Space is essentially a Python (or C++, and so on) application running within a Docker container, seamlessly orchestrated across a cluster of hosts using Kubernetes. This service detects faces in images, providing these detections in different ways.

## About :smile:

> YuNet is a light-weight, fast and accurate face detection model, which achieves 0.834(AP_easy), 0.824(AP_medium), 0.708(AP_hard) on the WIDER Face validation set. [See more](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)

The model is downloaded using the script [`etc/model/download_models.sh`](https://github.com/labvisio/is-face-detector/blob/master/etc/model/download_models.sh).

## Streams :camera:

A stream is a program that consumes messages with a specific topic, processes them, and publishes messages in other topics, so if another service wants to use the informations provided by this service, it can simply subscribe to receive messages with the topic of interest. The python script responsible for the stream in the table below can be found in [`src/is_face_detector/stream.py`](https://github.com/labvisio/is-face-detector/blob/master/src/is_face_detector/stream.py).

| Name | ⇒ Input | Output  ⇒ | Description |
| ---- | ------- | --------- | ----------- |
| Face.Detection | :incoming_envelope: **topic:** `CameraGateway.(camera_id).Frame` <br> :gem: **schema:** [Image] | :incoming_envelope: **topic:**  `FaceDetector.(camera_id).Detection` <br> :gem: **schema:** [ObjectAnnotations] | Detects face on images published by cameras and publishes an ObjectAnnotations message containing all the detected faces. |
| Face.Detection | :incoming_envelope: **topic:** `CameraGateway.(camera_id).Frame` <br> :gem: **schema:** [Image]| :incoming_envelope: **topic:** `FaceDetector.(camera_id).Rendered` <br> :gem: **schema:** [Image]| After detection, faces are drew on input image and published for visualization.|

- Note: run the `is-face-detector-stream` in container to use this function.

## RPCs :camera_flash:

The RPC, or Remote Procedure Call, provided here acts as a remote server that binds a specific function to a topic. You can process an [Image] by sending the message to the topic of this service. It will be processed and you will receive a response, which can be the faces detected in an [ObjectAnnotations], error, timeout, etc... The python script responsible for the RPC in the table below can be found in [`src/is_face_detector/rpc.py`](https://github.com/labvisio/is-face-detector/blob/master/src/is_face_detector/rpc.py).

| Service | Request | Reply |  Description |
| ------- | ------- | ----- | ------------ |
| :incoming_envelope: **topic:** `FaceDetector.Detect`| :gem: **schema:** [Image] | :gem: **schema:** [ObjectAnnotations] | Same purpose of stream shown above, but offered with a RPC server. |

- Note: run the `is-face-detector-rpc` in container to use this function.

## Configuration :gear:

The behavior of the service can be customized by passing a JSON configuration file as the first argument, e.g: `is-face-detector-stream config.json`. The schema for this file can be found in [`is_face_detector/conf/options.proto`](https://github.com/labvisio/is-face-detector/blob/master/is_face_detector/conf/options.proto).

An example configuration file can be found in [`etc/conf/options.json`](https://github.com/labvisio/is-face-detector/blob/master/etc/conf/options.json).

## Developing :hammer_and_wrench:

The project structure follows as:

```bash
.
├── etc
│   ├── conf
│   │   └── options.json
│   ├── docker
│   │   └── Dockerfile
│   ├── images
│   │   └── face.png
│   ├── k8s
│   │   └── deployment.yaml
│   └── model
│       └── download_models.sh
├── examples
│   └── request.py
├── is_face_detector
│   ├── conf
│   │   ├── __init__.py
│   │   ├── options_pb2.py
│   │   ├── options_pb2.pyi
│   │   └── options.proto
│   ├── detector.py
│   ├── __init__.py
│   ├── py.typed
│   ├── rpc.py
│   ├── stream_channel.py
│   ├── stream.py
│   └── utils.py
├── README.md
├── setup.cfg
└── setup.py
```

* [`etc/conf/options.json`](https://github.com/labvisio/is-face-detector/blob/master/etc/conf/options.json): Example of JSON configuration file. Also used as default if none is passed;

* [`etc/docker/Dockerfile`](https://github.com/labvisio/is-face-detector/blob/master/etc/docker/Dockerfile): Dockerfile with the instructions to build a docker image with this application;

* [`etc/k8s`](https://github.com/labvisio/is-face-detector/blob/master/etc/k8s): Example of yaml files indicating how to deploy the docker container of this application into a kubernetes cluster;

* [`etc/images`](https://github.com/labvisio/is-face-detector/blob/master/etc/images): examples of detection;

* [`etc/model/download_models.sh`](https://github.com/labvisio/is-face-detector/blob/master/etc/model/download_models.sh): shell script used to download model;

* [`is_face_detector`](https://github.com/labvisio/is-face-detector/blob/master/src/is_face_detector): python module with all the scripts;

* [`is_face_detector/stream.py`](https://github.com/labvisio/is-face-detector/blob/master/src/is_face_detector/stream.py): main python script for a Stream behavior;

* [`is_face_detector/rpc.py`](https://github.com/labvisio/is-face-detector/blob/master/src/is_face_detector/rpc.py): main python script for a RPC behavior;

* [`is_face_detector/conf/options.proto`](https://github.com/labvisio/is-face-detector/blob/master/is_face_detector/conf/options.proto): .proto file describing the schema of the options that can be passed to change the behavior of the service;

* [`setup.py`](setup.py): python file describing the module/package installed has been packaged and distributed with Distutils, which is the standard for distributing Python Modules.


### is-wire-py :incoming_envelope:

For a service to communicate with another, it uses a message-based protocol ([AMQP](https://github.com/celery/py-amqp)) which depends of a broker to receive and deliver all messages ([RabbitMQ](https://www.rabbitmq.com/)).

A python package was developed to abstract the communication layer implementing a publish/subscribe middleware, know as [is-wire-py](https://github.com/labvisio/is-wire-py). There you can find basic examples of message sending and receiving, or creating an RPC server, tracing messages, etc.


### Protocol Buffer :gem:

Every message on IS is standardized using [Protocol Buffer](https://developers.google.com/protocol-buffers). The schemas are defined at [is-msgs](https://github.com/labvisio/is-msgs). 

In this project, Procol Buffers are also used to define the [`options`](https://github.com/labvisio/is-face-detector/blob/master/is_face_detector/conf/options.proto) that are going to be loaded during runtime. The program will parse a [`json`](https://github.com/labvisio/is-face-detector/blob/master/etc/conf/options.json) into a Protocol Buffer Object and guarantee that it has a specific structure. **`You don't need do it this way if you don't want to`**, you can simply load the json as a dictionary during runtime.

### Docker <img alt="docker" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/docker/docker.png" />

To run the application into kubernetes platform, it must be packaged in the right format which is a [docker container](https://www.docker.com/resources/what-container). A docker container can be initialized from a docker image, the instructions to build the docker image are at [`etc/docker/Dockerfile`](https://github.com/labvisio/is-face-detector/blob/master/etc/docker/Dockerfile).

To be available to the kubernetes cluster, the docker image must be stored on [dockerhub](https://hub.docker.com/), to build the image locally and push to dockerhub:

```bash
docker build -f etc/docker/Dockerfile -t <user>/is-face-detector:<version> .
docker push <user>/is-face-detector:<version>
```

The docker image used here supports any application in python that uses [OpenCV]. Your application may not run because the image docker doesn't contain some library, in this case it will be necessary to edit the [`etc/docker/Dockerfile`](https://github.com/labvisio/is-face-detector/blob/master/etc/docker/Dockerfile) and rebuild it to install what you need or to use another base image. 

### Kubernetes <img alt="k8s" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/kubernetes/kubernetes.png" />

Make sure you have [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) installed and the right `~/.kube/config` file to be able to interact with the cluster.

Deploy the stream application:

```bash
kubectl apply -f etc/k8s/deployment.yaml
```

The `.yaml` file describes two things:
* a deployment;
* a configmap;

A deployment is a way to run our application and guarantee that an N number of replicas will be running. The configmap allows load the options you desires when deploying into the kubernetes platform. See more about [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and [confimap](https://kubernetes.io/docs/concepts/configuration/configmap/).

<!-- Links -->

[Image]: https://github.com/labvisio/is-msgs/tree/master/docs/README.md#is.vision.Image
[ObjectAnnotations]: https://github.com/labvisio/is-msgs/tree/master/docs/README.md#is.vision.ObjectAnnotations
[OpenCV]: https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html
