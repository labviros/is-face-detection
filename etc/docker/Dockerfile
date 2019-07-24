## First stage
FROM python:3.6-slim as build_step

## Download wget to get the model file
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget

## Download the model file
WORKDIR /opt/is
RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml  

## Fetch dependencies
WORKDIR /tmp
ADD . /tmp/
RUN pip wheel --wheel-dir=/root/wheels .
RUN rm -rf /tmp/*

## Second stage
FROM python:3.6-slim as package_step

## Copy the model
COPY --from=build_step /opt/is /opt/is

## Copy the dependencies
COPY --from=build_step /root/wheels /root/wheels

## Necessary dependencies to run OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 libxext6 libxrender-dev libglib2.0-0

## Copy the application 
WORKDIR /opt/is
COPY src/ src
COPY setup.py ./
COPY etc/conf/options.json ./

## Collect the dependecies
RUN pip install \ 
    --find-links=/root/wheels \ 
    .

CMD ["is-face-detector"]
