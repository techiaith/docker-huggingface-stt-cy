default: build

$(eval DEVICE = cpu)
#$(eval DEVICE = gpu)


config:	
	$(eval DOCKER_COMPOSE = docker compose -f docker-compose.${DEVICE}.yml)

up: config
	sudo rm -rf ${PWD}/logs
	mkdir -p ${PWD}/logs/
	mkdir -p ${PWD}/recordings/
	mkdir -p ${PWD}/redis_data/
	${DOCKER_COMPOSE} up -d --build && ${DOCKER_COMPOSE} logs -f


down: config
	${DOCKER_COMPOSE} down


