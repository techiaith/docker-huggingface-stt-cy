default: build

$(eval DEVICE = cpu)
#$(eval DEVICE = gpu)

config:
	# to use a local model, provide the full /models/.... path for WAV2VEC2_MODEL_NAME and 
	# leave the MODEL_VERSION blank empty string.
	#$(eval WAV2VEC2_MODEL_NAME = techiaith/wav2vec2-xlsr-ft-cy)
	$(eval WAV2VEC2_MODEL_NAME = techiaith/wav2vec2-xls-r-1b-ft-cy)
	$(eval WAV2VEC2_MODEL_VERSION = 22.06)
	mkdir -p ${PWD}/data/
	mkdir -p ${PWD}/tmp/



build: config
	docker build --rm -f Dockerfile.${DEVICE} -t techiaith/wav2vec2-inference-device .
	docker build --rm -t techiaith/wav2vec2-inference \
		--build-arg WAV2VEC2_MODEL_NAME=${WAV2VEC2_MODEL_NAME} \
		--build-arg MODEL_VERSION=${WAV2VEC2_MODEL_VERSION} \
		.

run: config run-${DEVICE}

run-gpu:
	docker run --gpus all --name techiaith-wav2vec2-inference-${DEVICE} \
		--restart=always \
		-it \
		-v ${PWD}/data/:/data \
		-v ${PWD}/tmp/:/tmp \
                techiaith/wav2vec2-inference


run-cpu:
	docker run --name techiaith-wav2vec2-inference-${DEVICE} \
		--restart=always \
		-it \
		-v ${PWD}/data/:/data \
		-v ${PWD}/tmp/:/tmp \
                techiaith/wav2vec2-inference


stop: config
	-docker stop techiaith-wav2vec2-inference-${DEVICE}
	-docker rm techiaith-wav2vec2-inference-${DEVICE}


clean: config stop
	-docker rmi techiaith/wav2vec2-inference

