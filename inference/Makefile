default: build


config:
	$(eval WAV2VEC2_MODEL_NAME = techiaith/wav2vec2-xlsr-ft-cy)
	$(eval MODEL_VERSION = 21.08)


build: config
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-cy \
		--build-arg WAV2VEC2_MODEL_NAME=${WAV2VEC2_MODEL_NAME} \
		--build-arg MODEL_VERSION=${MODEL_VERSION} \
		.


run: config
	mkdir -p ${PWD}/recordings/
	docker run --name techiaith-wav2vec2-xlsr-ft-cy \
		--restart=always \
		-it \
		-v ${PWD}/models/:/models \
		-v ${PWD}/recordings/:/recordings \
		techiaith/wav2vec2-xlsr-ft-cy


stop: config
	-docker stop techiaith-wav2vec2-xlsr-ft-cy
	-docker rm techiaith-wav2vec2-xlsr-ft-cy


clean: config stop
	-docker rmi techiaith/wav2vec2-xlsr-ft-cy
