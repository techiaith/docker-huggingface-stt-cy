#
FROM techiaith/wav2vec2-xlsr-ft-cy
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University, Language Technologies Unit

LABEL maintainer="techiaith"
LABEL repository="wav2vec2-xlsr-ft-cy-server"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake  \
    python3 python3-pip python3-setuptools python3-dev curl zip zlib1g-dev vim \
    ffmpeg sox alsa-utils \
 && python3 -m pip install --upgrade pip

# Install local Python files and dependencies..
RUN mkdir -p /wav2vec2-server && \
    mkdir -p /var/log/wav2vec2

WORKDIR /wav2vec2-server

COPY python/requirements.txt /wav2vec2-server/
RUN pip3 install -r requirements.txt 

COPY python /wav2vec2-server/

EXPOSE 8008

CMD ["/bin/bash", "-c", "/wav2vec2-server/start.sh"]
