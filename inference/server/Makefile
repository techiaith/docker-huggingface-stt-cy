default: build


config:	
	$(eval PORT_NUMBER = 5511)


build: config
	docker build --rm -t techiaith/wav2vec2-xlsr-ft-server-cy .


run: config
	mkdir -p ${PWD}/log/
	mkdir -p ${PWD}/recordings/
	docker run --gpus all --name techiaith-wav2vec2-xlsr-ft-server-cy \
		--restart=always \
		-it -d -p ${PORT_NUMBER}:8008 \
		-v ${PWD}/recordings/:/recordings \
		-v ${PWD}/../models/:/models \
		-v ${PWD}/log/:/var/log/wav2vec2 \
		techiaith/wav2vec2-xlsr-ft-server-cy


bash: config
	docker exec -it techiaith-wav2vec2-xlsr-ft-server-cy bash


stop: config
	-docker stop techiaith-wav2vec2-xlsr-ft-server-cy
	-docker rm techiaith-wav2vec2-xlsr-ft-server-cy
	rm -rf ${PWD}/log


clean: config stop
	-docker rmi techiaith/wav2vec2-xlsr-ft-server-cy
