.PHONY: build generate_config preprocess process

build:
	docker build -t helikite .

generate_config:
	docker run \
	    -v ./inputs:/app/inputs \
	    -v ./outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest generate_config

preprocess:
	docker run \
	    -v ./inputs:/app/inputs \
	    -v ./outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest preprocess

process:
	docker run \
	    -v ./inputs:/app/inputs \
	    -v ./outputs:/app/outputs \
	    ghcr.io/eerl-epfl/helikite-data-processing:latest
