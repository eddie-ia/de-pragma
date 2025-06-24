# Envs
DOCKER_IMAGE_NAME=dev-pragma
DOCKERFILE=Dockerfile
CONTAINER_WORKDIR=/app
CURDIR := $(abspath .)

# Build del contenedor y entrar en el
run:
	docker build -t $(DOCKER_IMAGE_NAME) -f $(DOCKERFILE) .
	docker run --rm -it -v "$(CURDIR):$(CONTAINER_WORKDIR)" -w $(CONTAINER_WORKDIR) $(DOCKER_IMAGE_NAME)

# Solo build
build:
	docker build -t $(DOCKER_IMAGE_NAME) -f $(DOCKERFILE) .

# Solo correr contenedor
docker-run:
	docker run --rm -it -v "$(CURDIR):$(CONTAINER_WORKDIR)" -w $(CONTAINER_WORKDIR) $(DOCKER_IMAGE_NAME)

# Limpiar salida
clean:
	rm -f outputs/*.db
