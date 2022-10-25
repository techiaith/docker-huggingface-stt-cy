FROM techiaith/wav2vec2-inference

RUN git clone https://github.com/marian-nmt/moses-scripts.git /usr/local/bin/moses-scripts

WORKDIR /wav2vec2-worker

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT celery -A worker worker --loglevel=info
