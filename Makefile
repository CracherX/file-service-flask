IMAGE_NAME = cracher/file-service-flask
DOCKERFILE = Dockerfile
CONTEXT = .

tag = $(shell cat $(CONTEXT)/version.txt)

IMAGE = $(IMAGE_NAME):$(tag)

CONFIG_HOST = ./config.yaml
CONFIG_CONTAINER = /config.yaml

build:
	@docker build -f $(DOCKERFILE) -t $(IMAGE) $(CONTEXT)

pull:
	@docker pull $(IMAGE)

push:
	@docker push $(IMAGE)

run:
	@docker run --volume $(CONFIG_HOST):$(CONFIG_CONTAINER) $(IMAGE)