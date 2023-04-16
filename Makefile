.PHONY: build generate_config preprocess process

build:
	docker build -t helikite .

generate_config:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    helikite:latest generate_config

preprocess:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    helikite:latest preprocess

process:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    helikite:latest