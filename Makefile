.PHONY: build generate_config preprocess process

build:
	docker build -t helikite .

generate_config:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest generate_config

preprocess:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest preprocess

process:
	docker run \
	    -v $(shell pwd)/inputs:/app/inputs \
	    -v $(shell pwd)/outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest
