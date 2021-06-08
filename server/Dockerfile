FROM ubuntu:20.04
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University, Language Technologies Unit

LABEL maintainer="techiaith"
LABEL repository="wav2vec2-xlsr-ft-cy-server"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake  \
    python3 python3-setuptools python3-pip python3-dev curl zip zlib1g-dev vim \
 && python3 -m pip install --upgrade pip

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB:en
ENV LC_ALL cy_GB.UTF-8

# Install local Python files and dependencies..
RUN mkdir -p /wav2vec2-server && \
    mkdir -p /var/log/wav2vec2

WORKDIR /wav2vec2-server
COPY python /wav2vec2-server/
RUN pip3 install -r requirements.txt 

# Install ctcdecoder..
RUN git clone --recursive https://github.com/parlance/ctcdecode.git /tmp/ctcdecode \
 && cd /tmp/ctcdecode && pip3 install .

EXPOSE 8008

#
ARG MODEL_DOMAIN
ARG MODEL_VERSION
ARG WAV2VEC2_MODEL_NAME
ARG KENLM_MODEL_NAME

#
ENV MODEL_VERSION=${MODEL_VERSION}
ENV MODEL_DOMAIN=${MODEL_DOMAIN}
ENV WAV2VEC2_MODEL_NAME=${WAV2VEC2_MODEL_NAME}
ENV KENLM_MODEL_NAME=${KENLM_MODEL_NAME}

CMD ["/bin/bash", "-c", "/wav2vec2-server/start.sh"]
