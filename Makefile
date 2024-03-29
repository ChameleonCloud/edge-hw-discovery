IMAGE_NAME = edge_hw_discovery

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) .
