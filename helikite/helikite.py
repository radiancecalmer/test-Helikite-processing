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
    fc = getattr(config, fc_yaml['config'])



    # POC: Flight computer to export
    fcdf = pd.read_csv(
        fc_yaml['file'],
        dtype=fc.dtype,
        na_values=fc.na_values,
        header=fc.header,
        delimiter=fc.delimiter,
        lineterminator=fc.lineterminator,
        comment=fc.comment,
        names=fc.names,
        index_col=fc.index_col,
    )
    fcdf['DateTime'] = pd.to_datetime(fcdf['DateTime'], unit='s')


    fig = go.Figure()

    # Add TEMPBox
    fig.add_trace(
        go.Scatter(
            x=fcdf.DateTime,
            y=fcdf.TEMPbox,
            name="TEMPBox"))

    # Add TEMPBox
    fig.add_trace(
        go.Scatter(
            x=fcdf.DateTime,
            y=fcdf.vBat,
            name="vBat"))

    fig.update_layout(title="Flight Computer")

    # Create a folder with the current UTC time in outputs
    output_path_with_time = os.path.join(config.constants.OUTPUTS_FOLDER,
                                    datetime.datetime.utcnow().isoformat())
    os.makedirs(output_path_with_time)
    with open(os.path.join(output_path_with_time,
                           config.constants.HTML_OUTPUT_FILENAME), 'w') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs=True))

    export_yaml_config(
        yaml_config,
        os.path.join(output_path_with_time, config.constants.CONFIG_FILE)
    )



# If docker arg 'preprocess' given, then run the preprocess function
if len(sys.argv) > 1 and sys.argv[1] == 'preprocess':
    print("TRUE!", sys.argv[0], sys.argv)
    preprocess()
elif __name__ == '__main__':
    main()



