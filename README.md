# helikite-data-processing
Code to merge data from helikite and produce quicklooks and data quality checks during campaigns


### Docker

1. Build the docker image

``` bash
docker build -t helikite .
```

2. Place a config file in the input directory with the csv/txt files from the sensors. A template can be found in the root directory `config.yaml`. Then populate the yaml file locations with the sensors using the `preprocess`
argument in the docker image.

``` bash
docker run -v ./inputs:/app/inputs helikite:latest preprocess
```

3. Generate the plots and build the export by running the previous step
**without** `preprocess`.

``` bash
docker run \
    -v ./inputs:/app/inputs \
    -v ./outputs:/app/outputs \
    helikite:latest
```
