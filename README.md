# Face Detector Service
[![](https://img.shields.io/docker/cloud/automated/labviros/is-face-detector?style=flat-square)](https://hub.docker.com/r/labviros/is-face-detector)
[![](https://img.shields.io/docker/cloud/build/labviros/is-face-detector?style=flat-square)](https://hub.docker.com/r/labviros/is-face-detector)
[![](https://img.shields.io/docker/pulls/labviros/is-face-detector?style=flat-square)](https://hub.docker.com/r/labviros/is-face-detector)
[![](https://img.shields.io/github/v/tag/labviros/is-face-detector?style=flat-square)](https://github.com/labviros/is-face-detector/tags)
[![](https://img.shields.io/docker/image-size/labviros/is-face-detector?style=flat-square)](https://hub.docker.com/r/labviros/is-face-detector)

![Example Image](https://github.com/labviros/is-face-detector/blob/master/etc/images/face.png)


In a simplified way, a service on the Intelligent Space is a python (or cpp, etc.) application running in a docker container which is orchestrated on a kubernetes platform across a set of hosts.

This service detects faces in images, providing these detections in different ways. It runs on **CPU**.

## About :smile:

> Object Detection using Haar feature-based cascade classifiers is an effective object detection method proposed by Paul Viola and Michael Jones in their paper, "Rapid Object Detection using a Boosted Cascade of Simple Features" in 2001. It is a machine learning based approach where a cascade function is trained from a lot of positive and negative images. It is then used to detect objects in other images. [See more](https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html)

In the link above you can find an explanation and simple examples about Object Detection using Haar feature-based cascade classifiers.

[opencv/data/haarcascades](https://github.com/opencv/opencv/tree/master/data/haarcascades) already contains many pre-trained classifiers for face, eyes, smiles, etc. Here we provide cascade classifiers only for face detection:

* `haarcascade_frontalface_default.xml`
* `haarcascade_frontalface_alt.xml`
* `haarcascade_frontalface_alt2.xml`
* `haarcascade_frontalface_alt_tree.xml`

The files are download using the script in [`etc/model/download_models.sh`](https://github.com/labviros/is-face-detector/blob/master/etc/model/download_models.sh). You can choose the scale factor, minimal neighbors and minimal size for the cascade classifier of your choice.

## Streams :camera:

A stream is a program that consumes messages with a specific topic, processes them, and publishes messages in other topics, so if another service wants to use the informations provided by this service, it can simply subscribe to receive messages with the topic of interest.

The python script responsible for the stream in the table below can be found in [`src/is_face_detector/stream.py`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector/stream.py).

| Name | ⇒ Input | Output  ⇒ | Description |
| ---- | ------- | --------- | ----------- |
| Face.Detection | :incoming_envelope: **topic:** `CameraGateway.(camera_id).Frame` <br> :gem: **schema:** [Image] | :incoming_envelope: **topic:**  `FaceDetector.(camera_id).Detection` <br> :gem: **schema:** [ObjectAnnotations] | Detects face on images published by cameras and publishes an ObjectAnnotations message containing all the detected faces. |
| Face.Detection | :incoming_envelope: **topic:** `CameraGateway.(camera_id).Frame` <br> :gem: **schema:** [Image]| :incoming_envelope: **topic:** `FaceDetector.(camera_id).Rendered` <br> :gem: **schema:** [Image]| After detection, faces are drew on input image and published for visualization.|

- Note: run the `is-face-detector-stream` in container to use this function.

## RPCs :camera_flash:

The RPC, or Remote Procedure Call, provided here acts as a remote server that binds a specific function to a topic. You can process an [Image] by sending the message to the topic of this service. It will be processed and you will receive a response, which can be the faces detected in an [ObjectAnnotations], error, timeout, etc...

The python script responsible for the RPC in the table below can be found in [`src/is_face_detector/rpc.py`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector/rpc.py).

| Service | Request | Reply |  Description |
| ------- | ------- | ----- | ------------ |
| :incoming_envelope: **topic:** `FaceDetector.Detect`| :gem: **schema:** [Image] | :gem: **schema:** [ObjectAnnotations] | Same purpose of stream shown above, but offered with a RPC server. |

- Note: run the `is-face-detector-rpc` in container to use this function.

## Configuration :gear:

The behavior of the service can be customized by passing a JSON configuration file as the first argument, e.g: `is-face-detector-stream config.json`. The schema for this file can be found in [`src/conf/options.proto`](https://github.com/labviros/is-face-detector/blob/master/src/conf/options.proto).

An example configuration file can be found in [`etc/conf/options.json`](https://github.com/labviros/is-face-detector/blob/master/etc/conf/options.json).

## Developing :hammer_and_wrench:

The project structure follows as:

```bash
.
├── etc
│   ├── conf
│   │   └── options.json
│   ├── docker
│   │   └── Dockerfile
│   ├── images
│   │   └── face.png
│   ├── k8s
│   │   ├── deployment.yaml
│   │   └── ...
│   └── model
│       └── download_models.sh
├── README.md
├── setup.py
└── src
    ├── conf
    │   ├── generate_pb.sh
    │   └── options.proto
    └── is_face_detector
        ├── face_detector.py
        ├── image_tools.py
        ├── __init__.py
        ├── options_pb2.py
        ├── rpc.py
        ├── stream_channel.py
        ├── stream.py
        └── utils.py
```

* [`etc/conf/options.json`](https://github.com/labviros/is-face-detector/blob/master/etc/conf/options.json): Example of JSON configuration file. Also used as default if none is passed;

* [`etc/docker/Dockerfile`](https://github.com/labviros/is-face-detector/blob/master/etc/docker/Dockerfile): Dockerfile with the instructions to build a docker image containing this application;

* [`etc/k8s`](https://github.com/labviros/is-face-detector/blob/master/etc/k8s): Example of yaml files indicating how to deploy the docker container of this application into a kubernetes cluster;

* [`etc/images`](https://github.com/labviros/is-face-detector/blob/master/etc/images): examples of detection;

* [`etc/model/download_models.sh`](https://github.com/labviros/is-face-detector/blob/master/etc/model/download_models.sh): shell script used to download the Haar feature-based cascade classifiers from opencv;

* [`src/is_face_detector`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector): python module with all the scripts;

* [`src/is_face_detector/stream.py`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector/stream.py): main python script for a Stream behavior;

* [`src/is_face_detector/rpc.py`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector/rpc.py): main python script for a RPC behavior;

* [`src/conf/options.proto`](https://github.com/labviros/is-face-detector/blob/master/src/conf/options.proto): .proto file describing the schema of the options that can be passed to change the behavior of the service;

* [`src/conf/generate_pb.sh`](https://github.com/labviros/is-face-detector/blob/master/src/conf/generate_pb.sh): shell script used to generate the file [`src/is_face_detector/options_pb2.py`](https://github.com/labviros/is-face-detector/blob/master/src/is_face_detector/options_pb2.py), that contains python classes indicating the schema of our options defined at [`src/conf/options.proto`](https://github.com/labviros/is-face-detector/blob/master/src/conf/options.proto);

* [`setup.py`](setup.py): python file describing the module/package installed has been packaged and distributed with Distutils, which is the standard for distributing Python Modules.


### is-wire-py :incoming_envelope:

For a service to communicate with another, it uses a message-based protocol ([AMQP](https://github.com/celery/py-amqp)) which depends of a broker to receive and deliver all messages ([RabbitMQ](https://www.rabbitmq.com/)).

A python package was developed to abstract the communication layer implementing a publish/subscribe middleware, know as [is-wire-py](https://github.com/labviros/is-wire-py). There you can find basic examples of message sending and receiving, or creating an RPC server, tracing messages, etc.


### Protocol Buffer :gem:

Every message on IS is standardized using [Protocol Buffer](https://developers.google.com/protocol-buffers). The schemas are defined at [is-msgs](https://github.com/labviros/is-msgs). 

In this project, Procol Buffers are also used to define the [`options`](https://github.com/labviros/is-face-detector/blob/master/src/conf/options.proto) that are going to be loaded during runtime. The program will parse a [`json`](https://github.com/labviros/is-face-detector/blob/master/etc/conf/options.json) into a Protocol Buffer Object and guarantee that it has a specific structure. **`You don't need do it this way if you don't want to`**, you can simply load the json as a dictionary during runtime.

In case you need to make any change on options protobuf file, will be necessary to rebuild the python file related to it. For do that, simply run the script [`src/conf/generate_pb.sh`](https://github.com/labviros/is-face-detector/blob/master/src/conf/generate_pb.sh)

```bash
cd src/conf/
./generate_pb.sh
```

### Docker <img alt="docker" width="26px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/docker/docker.png" />

To run the application into kubernetes platform, it must be packaged in the right format which is a [docker container](https://www.docker.com/resources/what-container). A docker container can be initialized from a docker image, the instructions to build the docker image are at [`etc/docker/Dockerfile`](https://github.com/labviros/is-face-detector/blob/master/etc/docker/Dockerfile).

To be available to the kubernetes cluster, the docker image must be stored on [dockerhub](https://hub.docker.com/). Here, the repository on dockerhub in linked to this github repository. So every time we set a tag here, it triggers the build of the docker image. More about  [how to automate the build of the docker image on dockerhub](https://docs.docker.com/docker-hub/builds/).

It is not necessary to automate the build of the docker image. It is possible to build the image locally and push to dockerhub. For example,

```bash
docker build -f etc/docker/Dockerfile -t <user>/is-face-detector:<version> .
docker push <user>/is-face-detector:<version>
```

The docker image used here supports any application in python that uses [OpenCV]. If you need another module, specify on [`requirements.txt`](https://github.com/labviros/is-face-detector/blob/master/requirements.txt). Your application may not run because the image docker doesn't contain some library, in this case it will be necessary to edit the [`etc/docker/Dockerfile`](https://github.com/labviros/is-face-detector/blob/master/etc/docker/Dockerfile) and rebuild it to install what you need or to use another base image. 




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

[Image]: https://github.com/labviros/is-msgs/tree/master/docs/README.md#is.vision.Image
[ObjectAnnotations]: https://github.com/labviros/is-msgs/tree/master/docs/README.md#is.vision.ObjectAnnotations
[OpenCV]: https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html
