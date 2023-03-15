import sys
from preprocess import preprocess, read_yaml_config, export_yaml_config
import config
import pandas as pd
import plotly.graph_objects as go
import os
import datetime


def main():
    # Get the yaml config
    yaml_config = read_yaml_config(os.path.join(config.constants.INPUTS_FOLDER,
                                                config.constants.CONFIG_FILE))

    # Right now just something manual for proof of concept
    fc_yaml = yaml_config['instruments']['flight_computer']

    # List to add plots to that will end up being exported
    figures = []

    # Create a folder with the current UTC time in outputs
    output_path_with_time = os.path.join(
        config.constants.OUTPUTS_FOLDER,
        datetime.datetime.utcnow().isoformat())
    os.makedirs(output_path_with_time)

    # Go through each instrument and perform the
    for instrument, props in yaml_config['instruments'].items():
        instrument_obj = getattr(config, props['config'])
        instrument_file = props['file']

        if instrument_file is None:
            print(f"Skipping {instrument}: No file assigned!")
            continue
        else:
            print(f"Processing {instrument}: {instrument_file}")

        # Read data into dataframe
        df = pd.read_csv(
            instrument_file,
            dtype=instrument_obj.dtype,
            na_values=instrument_obj.na_values,
            header=instrument_obj.header,
            delimiter=instrument_obj.delimiter,
            lineterminator=instrument_obj.lineterminator,
            comment=instrument_obj.comment,
            names=instrument_obj.names,
            index_col=instrument_obj.index_col,
        )

        # Apply any corrections on the data
        df = instrument_obj.data_corrections(df)

        # Generate the plots and add them to the list
        figures.append(instrument_obj.create_plots(df))

        # Save dataframe to outputs folder
        df.to_csv(f"{os.path.join(output_path_with_time, instrument)}.csv")


    html_filename = os.path.join(output_path_with_time,
                                 config.constants.HTML_OUTPUT_FILENAME)
    print(f"Writing {len(figures)} figures to {html_filename}")
    # Write out all of the figures to HTML
    with open(html_filename, 'w') as f:
        # Write figures. They'll be sorted by the order they were added
        for fig in figures:
            if fig is not None:  # Don't process any Nones in case of empty figs
                f.write(fig.to_html(full_html=False, include_plotlyjs=True))

    export_yaml_config(
        yaml_config,
        os.path.join(output_path_with_time,
                        config.constants.CONFIG_FILE)
    )



if __name__ == '__main__':
    # If docker arg 'preprocess' given, then run the preprocess function
    if len(sys.argv) > 1 and sys.argv[1] == 'preprocess':
        print("TRUE!", sys.argv[0], sys.argv)
        preprocess()
    else:
        main()
