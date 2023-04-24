import sys
from processing import preprocess, sorting
from constants import constants
import instruments
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import datetime
import plots
from functools import reduce
import logging


# Define a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(constants.LOGLEVEL_CONSOLE)
console_handler.setFormatter(constants.LOGFORMAT_CONSOLE)
logging.getLogger().addHandler(console_handler)

# Define logger for this file
logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def main():
    # Get the yaml config
    yaml_config = preprocess.read_yaml_config(
        os.path.join(constants.INPUTS_FOLDER,
                     constants.CONFIG_FILE))

    # List to add plots to that will end up being exported
    figures_quicklook = []
    figures_qualitycheck = []

    # Create a folder with the current UTC time in outputs
    output_path_with_time = os.path.join(
        constants.OUTPUTS_FOLDER,
        datetime.datetime.utcnow().isoformat())
    output_path_instrument_subfolder = os.path.join(
        output_path_with_time, constants.OUTPUTS_INSTRUMENT_SUBFOLDER)
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

    time_trim_start = pd.to_datetime(yaml_config['global']['time_trim']['start'])
    time_trim_end = pd.to_datetime(yaml_config['global']['time_trim']['end'])

    ground_station = yaml_config['ground_station']

    plot_props = yaml_config['plots']

    # Keep list of names of instruments that were processed successfully
    # to assist with plotting
    successful_instruments = []

    # Go through each instrument and perform the operations on each instrument
    for instrument, props in yaml_config['instruments'].items():

        instrument_obj = getattr(instruments, props['config'])
        instrument_obj.add_yaml_config(props)

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

        # Generate the plots and add them to the list
        # figures = figures + instrument_obj.create_plots(df)

        # Save dataframe to outputs folder
        df.to_csv(
            f"{os.path.join(output_path_instrument_subfolder, instrument)}.csv"
        )

        # Prepare df for combining with other instruments
        df = instrument_obj.add_device_name_to_columns(df)

        # Add tuple of df and export order to df merge list
        all_export_dfs.append((df, instrument_obj.export_order,
                               instrument_obj.housekeeping_columns,
                               instrument_obj.export_columns,
                               instrument_obj.name))

    preprocess.export_yaml_config(
        yaml_config,
        os.path.join(output_path_with_time,
                        constants.CONFIG_FILE)
    )

    # Sort the export columns in their numerical hierarchy order
    all_export_dfs.sort(key=sorting.df_column_sort_key)

    master_export_cols = []
    master_housekeeping_cols = []

    # Merge all the dataframes together, first df is the master
    master_df, sort_id, hk_cols, export_cols, name = all_export_dfs[0]

    master_export_cols += export_cols    # Combine list of data export columns
    master_housekeeping_cols += hk_cols  # Combine list of housekeeping columns
    # Merge the rest
    for df, sort_id, hk_cols, export_cols, name in all_export_dfs[1:]:

        master_df = master_df.merge(
            df, how="outer", left_index=True, right_index=True)
        master_export_cols += export_cols
        master_housekeeping_cols += hk_cols

    all_instruments = [x[4] for x in all_export_dfs]

    logger.info(f"Merging the following instruments: {all_instruments}")

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

    # Plots
    figures_quicklook.append(plots.generate_altitude_plot(master_df))
    figures_quicklook.append(plots.generate_grid_plot(
        master_df, all_instruments))

    # Housekeeping pressure vars as qualitychecks
    figures_qualitycheck.append(
        plots.plot_scatter_from_variable_list_by_index(
            master_df, "Housekeeping pressure variables",
            [
                "flight_computer_housekeeping_pressure",
                ("msems_readings_housekeeping_pressure"
                 if "msems_readings" in all_instruments else None),
                ("msems_scan_housekeeping_pressure"
                 if "msems_scan" in all_instruments else None),
                ("stap_housekeeping_pressure"
                 if "stap" in all_instruments else None),
                ("smart_tether_housekeeping_pressure"
                 if "smart_tether" in all_instruments else None),
                ("pops_housekeeping_pressure"
                 if "pops" in all_instruments else None),
            ],
        )
    )

    # Same with just pressure vars
    figures_qualitycheck.append(
        plots.plot_scatter_from_variable_list_by_index(
            master_df, "Pressure variables",
            [
                "flight_computer_P_baro",
                ("msems_readings_pressure"
                 if "msems_readings" in all_instruments else None),
                ("msems_scan_press_avg"
                 if "msems_scan" in all_instruments else None),
                ("stap_sample_press_mbar"
                 if "stap" in all_instruments else None),
                ("smart_tether_P (mbar)"
                 if "smart_tether" in all_instruments else None),
                ("pops_P"
                 if "pops" in all_instruments else None),
            ],
        )
    )

    # Generate plots for qualitychecks based on their variable name in the
    # merged dataframe. The two parameter Tuple[List[str], str] represents the
    # list of variables, and the title given to the plot in the second parameter
    for variables, instrument in [
        (["flight_computer_vBat","flight_computer_TEMPbox"], "Flight Computer"),
        ((["flight_computer_TEMP1", "flight_computer_TEMP2",
          "smart_tether_T (deg C)"], "Smart Tether")
          if "smart_tether" in all_instruments else (
        ["flight_computer_TEMP1", "flight_computer_TEMP2"],
           "Flight Computer")),
        (["pops_POPS_Flow"], "POPS"
         ) if "pops" in all_instruments else (None, None),
        (["msems_readings_msems_errs", "msems_readings_mcpc_errs"],
         "MSEMS Readings") if "msems_readings" in all_instruments else (
        None, None),
    ]:
        if variables is not None:
            figures_qualitycheck.append(
                plots.plot_scatter_from_variable_list_by_index(
                    master_df, instrument, variables,
                )
            )


    if "msems_scan" in all_instruments:
        heatmaps = plots.generate_particle_heatmap(
            master_df,
            plot_props['heatmap']['msems_inverted'],
            plot_props['heatmap']['msems_scan'],)

        for figure in heatmaps:
            figures_quicklook.append(figure)

        if plot_props['msems_readings_averaged'] is not None and len(plot_props['msems_readings_averaged']):
            for title, times in plot_props['msems_readings_averaged'].items():
                fig = plots.generate_average_bin_concentration_plot(
                    master_df, title, times[0], times[1])
                figures_quicklook.append(fig)

    # Save quicklook and qualitycheck plots to HTML files
    quicklook_filename = os.path.join(output_path_with_time,
                                      constants.QUICKLOOK_PLOT_FILENAME)
    plots.write_plots_to_html(figures_quicklook, quicklook_filename)


    qualitycheck_filename = os.path.join(output_path_with_time,
                                         constants.QUALITYCHECK_PLOT_FILENAME)
    plots.write_plots_to_html(figures_qualitycheck, qualitycheck_filename)

if __name__ == '__main__':
    # If docker arg given, don't run main
    if len(sys.argv) > 1:
        if sys.argv[1] == 'preprocess':
            preprocess.generate_config(overwrite=False)  # Write conf file
            preprocess.preprocess()
        elif sys.argv[1] == 'generate_config':
            logger.info("Generating YAML configuration in input folder")
            preprocess.generate_config(overwrite=True)
        else:
            logger.error("Unknown argument. Options are: preprocess, generate_config")
    else:
        # If no args, run the main application
        main()
