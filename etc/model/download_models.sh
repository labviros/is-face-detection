#!/bin/bash

# Get super user privileges
if [[ $EUID != 0 ]]; then
    export wasnt_root=true
	sudo -E "$0" "$@"
fi

if [[ $EUID == 0 ]]; then   
    wget_installed=false
    if command -v wget > /dev/null ; then
        wget_installed=true
    else
        echo "|>>| wget required"
    fi

    if [[ -z `command -v wget` ]] || [[ $wget_installed == false ]]; then
        echo "|>>| installing wget...";
        apt-get update
        apt-get install --no-install-recommends -y wget ca-certificates
    fi
fi

if [[ $EUID != 0 || -z ${wasnt_root} ]]; then
    WGET="wget --retry-connrefused --read-timeout=20 --timeout=15 -t 0 --continue -c"
    FILES="face_detection_yunet_2023mar.onnx"

    for file in ${FILES}; do
        if [ -e $file ]; then
            echo "|>>| model $file exists, skipping download..."
        else
            url="https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/${file}"
            echo "|>>| downloading ${file} "
            $WGET $url
        fi
    done
fi
