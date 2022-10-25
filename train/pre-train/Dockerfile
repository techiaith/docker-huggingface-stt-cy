FROM nvidia/cuda:11.4.0-cudnn8-devel-ubuntu20.04

LABEL maintainer="techiaith"
LABEL repository="wav2vec2-xlsr-pretrain-cy"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake \
    python3 python3-setuptools python3-pip cython

RUN python3 -m pip install --upgrade pip 

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB:en
ENV LC_ALL cy_GB.UTF-8

RUN mkdir -p /wav2vec2-pre-train
WORKDIR /wav2vec2-pre-train

RUN pip3 install torch==1.9.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
COPY python/requirements.txt /wav2vec2-pre-train/
RUN pip3 install -r requirements.txt 

COPY python /wav2vec2-pre-train
WORKDIR /wav2vec2-pre-train

