default: build


build:
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-train-${USER} .

run: 
	docker run --gpus all --name techiaith-wav2vec2-xlsr-ft-train-${USER} \
		-it \
		--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
		-v ${PWD}/homedir/:/root \
		-v ${PWD}/data/:/data \
		-v ${PWD}/models/:/models \
		-v ${PWD}/python/:/xlsr-ft-train \
		techiaith/wav2vec2-xlsr-ft-train-${USER} bash

stop:
	-docker stop techiaith-wav2vec2-xlsr-ft-train-${USER}
	-docker rm techiaith-wav2vec2-xlsr-ft-train-${USER}

clean:
	-docker rmi techiaith/wav2vec2-xlsr-ft-train-${USER}
	sudo rm -rf homedir
	mkdir -p homedir
