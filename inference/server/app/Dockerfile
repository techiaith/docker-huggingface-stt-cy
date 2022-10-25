FROM techiaith/wav2vec2-inference

RUN mkdir -p /var/log/wav2vec2

WORKDIR /wav2vec2-server

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8008

CMD ["/bin/bash", "-c", "/wav2vec2-server/start.sh"]

