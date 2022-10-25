default: build

build:
	docker build --rm -t techiaith/wav2vec2-pre-train-${USER} .

run:
	mkdir -p homedir/datasets
	mkdir -p logs
	docker run --name techiaith-wav2vec2-pre-train-${USER}-tensorboard \
		--restart=always \
		-v ${PWD}/logs/:/logs \
		-d -p 6007:6006 \
		tensorflow/tensorflow \
		tensorboard --bind_all --logdir /logs
 
	docker run --gpus all --name techiaith-wav2vec2-pre-train-${USER} \
		-it \
		--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
		-v ${PWD}/homedir/:/root \
		-v ${PWD}/data/:/data \
		-v ${PWD}/logs/:/logs \
		-v ${PWD}/models/:/models \
		-v ${PWD}/python/:/wav2vec2-pre-train \
		techiaith/wav2vec2-pre-train-${USER} bash

stop:
	-docker stop techiaith-wav2vec2-pre-train-${USER}-tensorboard
	-docker stop techiaith-wav2vec2-pre-train-${USER}
	-docker rm techiaith-wav2vec2-pre-train-${USER}-tensorboard
	-docker rm techiaith-wav2vec2-pre-train-${USER}

clean: stop
	-docker rmi techiaith/wav2vec2-pre-train-${USER}
	sudo rm -rf homedir
	sudo rm -rf logs

tensorboard:
	python3 -m tensorboard.main serve --bind_all --logdir=logs/

