default: build

$(eval DEVICE = cpu)
#$(eval DEVICE = gpu)

config:
	# to use a local model, provide the full /models/.... path for WAV2VEC2_MODEL_NAME and 
	# leave the MODEL_VERSION blank empty string.
	$(eval WAV2VEC2_MODEL_NAME = techiaith/wav2vec2-xlsr-ft-cy)
	$(eval MODEL_VERSION = 21.08)
	mkdir -p ${PWD}/data/


build: config
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-cy-${USER} \
		--build-arg WAV2VEC2_MODEL_NAME=${WAV2VEC2_MODEL_NAME} \
		--build-arg MODEL_VERSION=${MODEL_VERSION} \
		.

run: config run-${DEVICE}

run-gpu:
	docker run --gpus all --name techiaith-wav2vec2-xlsr-ft-cy-${USER} \
		--restart=always \
		-it \
		-v ${PWD}/models/:/models \
		-v ${PWD}/data/:/data \
		techiaith/wav2vec2-xlsr-ft-cy-${USER}

run-cpu:
	docker run --name techiaith-wav2vec2-xlsr-ft-cy-${USER} \
		--restart=always \
		-it \
		-v ${PWD}/models/:/models \
		-v ${PWD}/data/:/data \
		techiaith/wav2vec2-xlsr-ft-cy-${USER}


fetch-test:
	if [ ! -d "data/corpws-profi-adnabod-lleferydd" ]; then \
	    mkdir -p data; \
	    cd data && git clone -b fersiwn2 --single-branch https://git.techiaith.bangor.ac.uk/data-porth-technolegau-iaith/corpws-profi-adnabod-lleferydd.git; \
	fi

stop: config
	-docker stop techiaith-wav2vec2-xlsr-ft-cy-${USER}
	-docker rm techiaith-wav2vec2-xlsr-ft-cy-${USER}


clean: config stop
	-docker rmi techiaith/wav2vec2-xlsr-ft-cy-${USER}

purge: clean
	sudo rm -rf models
