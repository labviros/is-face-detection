## First stage
FROM python:3.6-slim as build_step

## Download the models
WORKDIR /opt/is
COPY etc/model/download_models.sh ./download_models.sh
RUN bash ./download_models.sh && \
    rm download_models.sh

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
COPY requirements.txt ./
COPY etc/conf/options.json ./

## Collect the dependecies
RUN pip install \ 
    --find-links=/root/wheels \ 
    .

CMD ["is-face-detector-stream"]
