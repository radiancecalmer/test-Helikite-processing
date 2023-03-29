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
from functools import reduce
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
    all_export_dfs = []
    all_housekeeping_dfs = []

    # Go through each instrument and perform the operations on each instrument
    for instrument, props in yaml_config['instruments'].items():

        instrument_obj = getattr(config.instrument, props['config'])
        instrument_obj.add_yaml_config(props)

        if instrument_obj.filename is None:
            print(f"Skipping {instrument}: No file assigned!")
            continue
        else:
            print(f"Processing {instrument}: {instrument_obj.filename}")

        df = instrument_obj.read_data()

        # Modify the DateTime index based off the configuration offsets
        df = instrument_obj.set_time_as_index(df)

        # Apply any corrections on the data
        df = instrument_obj.data_corrections(df)

        # Create housekeeping pressure variable to help align pressure visually
        df = instrument_obj.set_housekeeping_pressure_offset_variable(
            df, column_name=config.constants.HOUSEKEEPING_VAR_PRESSURE
        )

        # Generate the plots and add them to the list
        figures = figures + instrument_obj.create_plots(df)

        df_housekeeping = instrument_obj.get_housekeeping_data(
            df,
            pressure_housekeeping_var=config.constants.HOUSEKEEPING_VAR_PRESSURE
        )
        df_export = instrument_obj.get_export_data(df)

        # Save dataframe to outputs folder
        df_export.to_csv(f"{os.path.join(output_path_with_time, instrument)}.csv")
        df_export.columns = f"{instrument}_" + df_export.columns.values

        # Add dataframes to list, with the export list is as a tuple
        # to sequence instruments in specific order
        df_housekeeping.columns = f"{instrument}_" + df_housekeeping.columns.values
        all_housekeeping_dfs.append(df_housekeeping)
        all_export_dfs.append((df_export, instrument_obj.export_order))

        print()


    export_yaml_config(
        yaml_config,
        os.path.join(output_path_with_time,
                        config.constants.CONFIG_FILE)
    )

    def sort_key(export_df):
        # Uses value in the second position of the tuple to define sort 'height'
        # ie. (df, 100) is sorted higher than (df, 50)

        if export_df[1] is None:
            # If no order set, push it to the end
            print(f"There is no sort key for columns {export_df[0].columns}. ")
            print("Placing them at the end.")
            return 999999

        return export_df[1]

    # Sort the export columns in their numerical hierarchy order
    all_export_dfs.sort(key=sort_key)

    master_export_df, sort_order = all_export_dfs[0]
    for df, sort_order in all_export_dfs[1:]:
        master_export_df = master_export_df.merge(
            df, how="outer", left_index=True, right_index=True)


    # Sort by the date index
    master_export_df.sort_index(inplace=True)
    master_export_df.to_csv(os.path.join(output_path_with_time,
                           config.constants.MASTER_CSV_FILENAME))


    master_housekeeping_df = all_housekeeping_dfs[0]
    for df in all_housekeeping_dfs[1:]:
        if len(df) > 0:
            master_housekeeping_df = master_housekeeping_df.merge(
                df, how="outer", left_index=True, right_index=True)

    # Sort by the date index
    master_housekeeping_df.sort_index(inplace=True)
    master_housekeeping_df.to_csv(
        os.path.join(output_path_with_time,
                     config.constants.HOUSEKEEPING_CSV_FILENAME))

    # Housekeeping vars
    figures.append(
        plots.plot_scatter_from_variable_list_by_index(
            master_housekeeping_df, "Housekeeping variables",
            [
                "flight_computer_TEMPbox",
                "flight_computer_vBat",
                "msems_readings_msems_errs",
                "msems_scan_msems_errs",
                "msems_readings_mcpc_errs",
                "msems_scan_mcpc_errs",
                "pops_POPS_Flow",
            ],
        )
    )

    # Housekeeping pressure vars
    figures.append(
        plots.plot_scatter_from_variable_list_by_index(
            master_housekeeping_df, "Housekeeping pressure variables",
            [
                "flight_computer_housekeeping_pressure",
                "msems_readings_housekeeping_pressure",
                "msems_scan_housekeeping_pressure",
                "stap_housekeeping_pressure",
                "smart_tether_housekeeping_pressure",
                "pops_housekeeping_pressure"
            ],
        )
    )

    # Pressure vars
    figures.append(
        plots.plot_scatter_from_variable_list_by_index(
            master_export_df, "Pressure variables",
            [
                "flight_computer_P_baro",
                "msems_readings_pressure",
                "msems_scan_press_avg",
                "stap_sample_press_mbar",
                "smart_tether_P (mbar)",
                "pops_P"
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
            generate_config(overwrite=False)  # Write conf file if doesn't exist
            preprocess()
        elif sys.argv[1] == 'generate_config':
            print("Generating YAML configuration in input folder")
            generate_config(overwrite=True)
        else:
            print("Unknown argument. Options are: preprocess, generate_config")
    else:
        # If no args, runt he main application
        main()
