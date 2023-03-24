import sys
from preprocess import (
    preprocess, read_yaml_config, export_yaml_config, generate_config
)
import config
import pandas as pd
import plotly.graph_objects as go
import os
import datetime
import plots
# from plots import plot_scatter_from_variable_list_by_index


def main():
    # Get the yaml config
    yaml_config = read_yaml_config(os.path.join(config.constants.INPUTS_FOLDER,
                                                config.constants.CONFIG_FILE))

    # List to add plots to that will end up being exported
    figures = []

    # Create a folder with the current UTC time in outputs
    output_path_with_time = os.path.join(
        config.constants.OUTPUTS_FOLDER,
        datetime.datetime.utcnow().isoformat())
    os.makedirs(output_path_with_time)

    # Append each df to this to eventually join on a key
    all_dfs = []

    # Go through each instrument and perform the operations on each instrument
    for instrument, props in yaml_config['instruments'].items():

        instrument_obj = getattr(config.instrument, props['config'])

        instrument_obj.filename = props['file']
        instrument_obj.date = props['date']

        if instrument_obj.filename is None:
            print(f"Skipping {instrument}: No file assigned!")
            continue
        else:
            print(f"Processing {instrument}: {instrument_obj.filename}")

        df = instrument_obj.read_data()

        # Apply any corrections on the data
        df = instrument_obj.data_corrections(df)

        # Generate the plots and add them to the list
        figures.append(instrument_obj.create_plots(df))

        # Save dataframe to outputs folder
        df.to_csv(f"{os.path.join(output_path_with_time, instrument)}.csv")
        # all_dfs.append(df)

        # Remove microseconds from timestamps so they fit better to other data
        df.set_index('DateTime', inplace=True)
        df.index = pd.to_datetime(df.index).round('s')
        # df.index = df.index.floor('S').tz_localize(None)

        if instrument == 'flight_computer':
            print("flight comp!")
            fc = df
        else:
            all_dfs.append((df, instrument))  # Append to join with instr. name
        # print(df['DateTime'].dtype)


    export_yaml_config(
        yaml_config,
        os.path.join(output_path_with_time,
                        config.constants.CONFIG_FILE)
    )
    for df, instrument_name in all_dfs:
        df.columns = f"{instrument_name}_" + df.columns.values
        fc = fc.merge(df, on='DateTime', how='outer',)

    # Sort by the date index
    fc.sort_index(inplace=True)
    fc.to_csv(f"{os.path.join(output_path_with_time, 'fc')}.csv")

    # Housekeeping vars
    figures.append(
        plots.plot_scatter_from_variable_list_by_index(
            fc, "Housekeeping variables",
            [
                "TEMPbox",
                "vBat",
                "msems_readings_msems_errs",
                "msems_scan_msems_errs",
                "msems_readings_mcpc_errs",
                "msems_scan_mcpc_errs",
                "pops_POPS_Flow",
            ],
        )
    )

    # Pressure vars
    figures.append(
        plots.plot_scatter_from_variable_list_by_index(
            fc, "Pressure variables",
            [
                "P_baro",
                "msems_readings_pressure",
                "msems_scan_press_avg",
                "stap_sample_press_mbar"
            ],
        )
    )

    html_filename = os.path.join(output_path_with_time,
                                 config.constants.HTML_OUTPUT_FILENAME)
    plots.write_plots_to_html(figures, html_filename)

if __name__ == '__main__':
    # If docker arg given, don't run main
    if len(sys.argv) > 1:
        if sys.argv[1] == 'preprocess':
            print("TRUE!", sys.argv[0], sys.argv)
            preprocess()
        elif sys.argv[1] == 'generate_config':
            print("Generating YAML configuration in input folder")
            generate_config()
        else:
            print("Unknown argument. Options are: preprocess, generate_config")
    else:
        # If no args, runt he main application
        main()
