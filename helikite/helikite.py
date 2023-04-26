import sys
from processing import preprocess, sorting
from constants import constants
import instruments
import pandas as pd
import os
import datetime
import plots
import logging
from typing import Dict, Any

# Define a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(constants.LOGLEVEL_CONSOLE)
console_handler.setFormatter(constants.LOGFORMAT_CONSOLE)
logging.getLogger().addHandler(console_handler)

# Define logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def main(
    config: Dict[str, Any],
    output_path: str = constants.OUTPUTS_FOLDER,
) -> None:
    ''' Main function to run the processing and plotting of data

    Parameters
    ----------
    config : Dict[str, Any]
        Dictionary of the configuration file

    Returns
    -------
    None

    '''

    # Create a folder with the current UTC time in outputs
    output_path_with_time = os.path.join(
        output_path, datetime.datetime.utcnow().isoformat()
    )
    output_path_instrument_subfolder = os.path.join(
        output_path_with_time, constants.OUTPUTS_INSTRUMENT_SUBFOLDER
    )
    os.makedirs(output_path_with_time)
    os.makedirs(output_path_instrument_subfolder)

    # Add a file logger
    logfile_handler = logging.FileHandler(os.path.join(output_path_with_time,
                                                       constants.LOGFILE_NAME))
    logfile_handler.setLevel(constants.LOGLEVEL_FILE)
    logfile_handler.setFormatter(constants.LOGFORMAT_FILE)
    logging.getLogger().addHandler(logfile_handler)

    # Append each df for merging
    all_export_dfs = []

    time_trim_start = pd.to_datetime(
        config['global']['time_trim']['start'])
    time_trim_end = pd.to_datetime(config['global']['time_trim']['end'])

    ground_station = config['ground_station']
    plot_props = config['plots']

    # Go through each instrument and perform the operations on each instrument
    for instrument, props in config['instruments'].items():

        instrument_obj = getattr(instruments, props['config'])
        instrument_obj.add_config(props)

        if instrument_obj.filename is None:
            logger.warning(f"Skipping {instrument}: No file assigned!")
            continue
        else:
            logger.info(f"Processing {instrument}: {instrument_obj.filename}")

        df = instrument_obj.read_data()

        # Modify the DateTime index based off the configuration offsets
        df = instrument_obj.set_time_as_index(df)

        # Using the time corrections from configuration, correct time index
        df = instrument_obj.correct_time_from_config(
            df, time_trim_start, time_trim_end
        )
        if len(df) == 0:
            logger.warning(f"Skipping {instrument}: No data in time range!")
            continue

        # Apply any corrections on the data
        df = instrument_obj.data_corrections(
            df,
            start_altitude=ground_station['altitude'],
            start_pressure=ground_station['pressure'],
            start_temperature=ground_station['temperature'],
            )

        # Create housekeeping pressure variable to help align pressure visually
        df = instrument_obj.set_housekeeping_pressure_offset_variable(
            df, column_name=constants.HOUSEKEEPING_VAR_PRESSURE
        )

        # Save dataframe to outputs folder
        df.to_csv(
            f"{os.path.join(output_path_instrument_subfolder, instrument)}.csv"
        )

        # Prepare df for combining with other instruments
        df = instrument_obj.add_device_name_to_columns(df)

        # Add tuple of df and export order to df merge list
        all_export_dfs.append((df, instrument_obj))

    preprocess.export_yaml_config(
        config,
        os.path.join(output_path_with_time, constants.CONFIG_FILE)
    )

    # Sort the export columns in their numerical hierarchy order and log
    all_export_dfs.sort(key=sorting.df_column_sort_key)
    logger.info("Instruments will be merged together with this column order:")
    logger.info("----------")
    for df, inst in all_export_dfs:
        logger.info(
            f"Instrument: {inst.name:20}"
            f"(Export order value: {inst.export_order})")

    master_export_cols = []
    master_housekeeping_cols = []

    # Merge all the dataframes together, first df is the master
    master_df, instrument = all_export_dfs[0]

    # Combine export and housekeeping columns
    master_export_cols += instrument.export_columns
    master_housekeeping_cols += instrument.housekeeping_columns

    # Merge the rest
    for df, instrument in all_export_dfs[1:]:
        logger.info(f'Merging instrument: {instrument.name}')
        master_df = master_df.merge(
            df, how="outer", left_index=True, right_index=True)
        master_export_cols += instrument.export_columns
        master_housekeeping_cols += instrument.housekeeping_columns

    all_instruments = [instrument for df, instrument in all_export_dfs]

    # Sort rows by the date index
    master_df.index = pd.to_datetime(master_df.index)
    master_df.sort_index(inplace=True)

    # Export data and housekeeping CSV files
    master_df[master_export_cols].to_csv(
        os.path.join(output_path_with_time,
                     constants.MASTER_CSV_FILENAME))

    master_df[master_housekeeping_cols].to_csv(
        os.path.join(output_path_with_time,
                     constants.HOUSEKEEPING_CSV_FILENAME))

    # Create all of the plots
    plots.campaign_2023(
        master_df, plot_props, all_instruments, output_path_with_time
    )


if __name__ == '__main__':
    # If docker arg given, don't run main
    if len(sys.argv) > 1:
        if sys.argv[1] == 'preprocess':
            # Run the preprocessing, generate config if it doesn't exist
            preprocess.generate_config(overwrite=False)  # Write conf file
            preprocess.preprocess()
        elif sys.argv[1] == 'generate_config':
            # Generate the config file (overwrite if it exists)
            logger.info("Generating YAML configuration in input folder")
            preprocess.generate_config(overwrite=True)
        else:
            logger.error("Unknown argument. Options are: preprocess, "
                         "generate_config")
    else:  # If no args, run the main application
        # Get the config from the YAML file in the input directory
        config = preprocess.read_yaml_config(
            os.path.join(constants.INPUTS_FOLDER, constants.CONFIG_FILE)
        )

        main(config)
