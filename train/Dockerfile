FROM nvidia/cuda:11.2.0-cudnn8-devel-ubuntu20.04

LABEL maintainer="techiaith"
LABEL repository="wav2vec2-xlsr-ft-cy"

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

RUN mkdir -p /xlsr-ft-train
WORKDIR /xlsr-ft-train

COPY python /xlsr-ft-train/
RUN pip3 install -r requirements.txt 

# Install KenLM
RUN git clone https://github.com/kpu/kenlm.git /usr/local/src/kenlm 
WORKDIR /usr/local/src/kenlm 
RUN mkdir -p build && cd build && cmake .. && make -j 4

ENV PATH="/usr/local/src/kenlm/build/bin:/usr/local/src/kenlm/scripts:${PATH}"

RUN git clone --recursive https://github.com/parlance/ctcdecode.git /tmp/ctcdecode \
 && cd /tmp/ctcdecode && pip3 install .

WORKDIR /xlsr-ft-train
