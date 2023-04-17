# helikite

This library aims to support Helikite campaigns by unifying data collected from fieldwork
and producing quicklooks on recorded data from instruments to assist with instrument
housekeeping and quality control.

## Getting started

There are three stages to the application. These are:

1. (Optional) Generate a config file in the `input` folder. This writes out a configuration
   file that the application will use to refer to instrument files and their individual
   configurations that have been defined in this library. This only needs to be run if
   there is no config file that exists in the input folder already, or if more instruments
   need to be added.

   **Note**: It will overwrite the config in the `input` folder.

   Once generated, the user may remove instruments that should not be considered in the
   preprocessing or processing stages (stage 2 and 3).

   This stage's command-line argument is: `generate_config`.

2. Scanning the input folder of raw instrument files and assigning them to the instrument
   configurations in the config file that were generated in stage 1. The configuration file
   is updated with the file location, and other instrument-specific metadata such as scan
   date (should it be located in the file header and not in a field -- see _Smart Tether_
   configuration)

   This stage's command-line argument is: `preprocess`.

   After this stage is complete, the user may edit the generated `config.yaml` by
   removing instruments or setting variables that will be used by the next stage.

3. Processing the input data files based on the config file in the same `input` folder,
   normalising the timestamps of each record, saving their outputs and generating plots
   in the `output` folder.

   Each time the application runs, it will create a UTC timestamped folder in the `output`
   folder with the processed input files, plots and a copy of the configuration file used.
   Therefore, the configuration file can be edited many times and running this step will
   not affect any previous output.

   This is the default behaviour of the application (no command-line arguments).

### Docker

1. Build the docker image

   This only needs to be built once unless there is a change in code.

   ```bash
   docker build -t helikite .
   ```

2. Generate project folders and config file

   Define two folders: `inputs` and `outputs`. These are mapped to the
   docker container with the left section of the `-v` argument
   (in the below example the relative paths are used
   `./inputs` and `./outputs`).

   Generate the configuration file in the `input` folder:

   ```bash
   docker run \
       -v ./inputs:/app/inputs \
       -v ./outputs:/app/outputs \
       helikite:latest generate_config
   ```

   Note: `helikite:latest` refers to the `latest` version of the docker
   image that was built in step 1. This is always the most recent image
   that was built. If If you would like to use an older build, find the image
   ID with the command `docker images helikite` and replace `latest` with it.

   ```bash
   $ docker images helikite

   REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
   helikite     latest    4a04184a12aa   9 days ago   497MB
   ```

3. Preprocess the configuration file

   Fill the metadata in the config.yaml by associating the files in the input
   directory to the known configurations in the library (such as determining
   instrument, date, etc)

   ```bash
   docker run \
       -v ./inputs:/app/inputs \
       -v ./outputs:/app/outputs \
       helikite:latest preprocess
   ```

4. Generate the plots and processed input files. These will be placed in the
   `output` folder that is defined here, in a directory based on the UTC time
   of when this command is run.

   ```bash
   docker run \
       -v ./inputs:/app/inputs \
       -v ./outputs:/app/outputs \
       helikite:latest
   ```

### Using the Makefile

Run the following commands as needed:

- To build the Docker image:

  ```
  make build
  ```

- To generate the configuration file in the `inputs` folder:

  ```
  make generate_config
  ```

- To preprocess the configuration file by filling the metadata:

  ```
  make preprocess
  ```

- To generate plots and processed input files, which will be placed in a timestamped directory within the `outputs` folder:

  ```
  make process
  ```
