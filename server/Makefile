default: build


transcribe-config:
	$(eval MODEL_DOMAIN = transcribe-cy)
	$(eval MODEL_VERSION = 21.05)
	$(eval WAV2VEC2_MODEL_NAME = techiaith_bangor/wav2vec2-xlsr-ft-cy)
	$(eval KENLM_MODEL_NAME = techiaith_bangor/kenlm-cy)
	$(eval PORT_NUMBER = 5511)


build: transcribe-config	
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-server:${MODEL_DOMAIN} \
		--build-arg MODEL_DOMAIN=${MODEL_DOMAIN} \
		--build-arg MODEL_VERSION=${MODEL_VERSION} \
		--build-arg WAV2VEC2_MODEL_NAME=${WAV2VEC2_MODEL_NAME} \
		--build-arg KENLM_MODEL_NAME=${KENLM_MODEL_NAME} \
		.


run: transcribe-config
	mkdir -p ${PWD}/log/${MODEL_DOMAIN}
	mkdir -p ${PWD}/recordings/${MODEL_DOMAIN}
	docker run --name techiaith-wav2vec2-xlsr-ft-server-${MODEL_DOMAIN} \
		--restart=always \
		-it -d -p ${PORT_NUMBER}:8008 \
		-v ${PWD}/../models/:/models \
		-v ${PWD}/log/${MODEL_DOMAIN}:/var/log/wav2vec2 \
		-v ${PWD}/recordings/${MODEL_DOMAIN}:/recordings \
		techiaith/wav2vec2-xlsr-ft-server:${MODEL_DOMAIN}


stop: transcribe-config
	-docker stop techiaith-wav2vec2-xlsr-ft-server-${MODEL_DOMAIN}
	-docker rm techiaith-wav2vec2-xlsr-ft-server-${MODEL_DOMAIN}
	rm -rf ${PWD}/log/${MODEL_DOMAIN}


clean: transcribe-config stop
	-docker rmi techiaith/wav2vec2-xlsr-ft-server:${MODEL_DOMAIN}
