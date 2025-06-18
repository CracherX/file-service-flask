IMAGE_NAME = cracher/file-service-flask
DOCKERFILE = Dockerfile
CONTEXT = .

tag = $(shell cat $(CONTEXT)/version.txt)

IMAGE = $(IMAGE_NAME):$(tag)
IMAGE_STATIC = $(IMAGE_NAME)-static:$(tag)

all: build

build:
	@docker build -f $(DOCKERFILE) -t $(IMAGE) $(CONTEXT)

pull:
	@docker pull $(IMAGE)

push:
	@docker push $(IMAGE)

run:
	@docker run $(IMAGE)