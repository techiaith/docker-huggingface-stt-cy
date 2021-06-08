default: build

TECHIAITH_RELEASE := 21.05


build:
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-train-${USER} .

run: 
	docker run --gpus all --name techiaith-wav2vec2-xlsr-ft-train-${USER} \
		-it \
		-v ${PWD}/homedir/:/root \
		-v ${PWD}/../models/:/models \
		-v ${PWD}/python/:/xlsr-ft-train \
		--env TECHIAITH_RELEASE=${TECHIAITH_RELEASE} \
		techiaith/wav2vec2-xlsr-ft-train-${USER} bash

stop:
	-docker stop techiaith-wav2vec2-xlsr-ft-train-${USER}
	-docker rm techiaith-wav2vec2-xlsr-ft-train-${USER}

clean:
	-docker rmi techiaith/wav2vec2-xlsr-ft-train-${USER}
	sudo rm -rf homedir
	mkdir -p homedir
