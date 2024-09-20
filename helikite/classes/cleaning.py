import pandas as pd
from typing import Any
import datetime
from helikite.instruments.base import Instrument
from helikite.constants import constants
import matplotlib.pyplot as plt


class Cleaner:
    def __init__(
        self,
        instruments: list[Instrument],
        input_folder: str,
        flight_date: datetime.date,
        time_trim_from: datetime.datetime | None = None,
        time_trim_to: datetime.datetime | None = None,
        time_offset: datetime.time = datetime.time(0, 0),
    ) -> None:
        self._instruments: list[Instrument] = []  # For managing in batches
        self.input_folder: str = input_folder
        self.flight_date: datetime.date = flight_date
        self.time_trim_from: datetime.datetime | None = time_trim_from
        self.time_trim_to: datetime.datetime | None = time_trim_to
        self.time_offset: datetime.time = time_offset
        self.pressure_column: str = constants.HOUSEKEEPING_VAR_PRESSURE

        # Create an attribute from each instrument.name
        for instrument in instruments:
            instrument.df_original = instrument.read_from_folder(
                input_folder, quiet=True
            )
            instrument.df = instrument.df_original.copy(deep=True)
            instrument.date = flight_date
            instrument.time_offset = {}
            instrument.time_offset["hour"] = time_offset.hour
            instrument.time_offset["minute"] = time_offset.minute
            instrument.time_offset["second"] = time_offset.second

            # Add the instrument to the Cleaner object and the list
            setattr(self, instrument.name, instrument)
            self._instruments.append(instrument)

        self.print_instruments()
        print("Each instrument has a df attribute, and a backup df_original.")

    def print_instruments(self) -> None:
        for instrument in self._instruments:
            print(f"Cleaner.{instrument.name} ({len(instrument.df)} records)")

    def set_pressure_column(
        self,
        column_name: str = constants.HOUSEKEEPING_VAR_PRESSURE,
    ) -> None:
        if column_name != constants.HOUSEKEEPING_VAR_PRESSURE:
            print("Updating pressure column to", column_name)
            self.pressure_column = column_name

        for instrument in self._instruments:
            try:
                instrument.df = (
                    instrument.set_housekeeping_pressure_offset_variable(
                        instrument.df, self.pressure_column
                    )
                )
                print("Set pressure column for", instrument.name)
            except Exception as e:
                print(
                    f"Error setting pressure column for {instrument.name}: {e}"
                )

    def set_time_as_index(self) -> None:
        for instrument in self._instruments:
            try:
                instrument.df = instrument.set_time_as_index(instrument.df)
                print("Set time as index for", instrument.name)
            except Exception as e:
                print(
                    f"Error setting time as index for {instrument.name}: {e}"
                )

    def correct_time(
        self,
        trim_start: pd.Timestamp | None = None,
        trim_end: pd.Timestamp | None = None,
    ) -> None:

        # If no trim start or end, use the class's time_trim_from/to values
        if trim_start is None:
            trim_start = self.time_trim_from
        if trim_end is None:
            trim_end = self.time_trim_to

        for instrument in self._instruments:
            try:
                temp_df = instrument.correct_time_from_config(
                    instrument.df, trim_start, trim_end
                )
                if len(instrument.df) == 0:
                    print(
                        f"Warning {instrument.name}: No data in time range! "
                        "No changes have been made."
                    )
                    continue

                instrument.df = temp_df
                print("Corrected time from config for", instrument.name)
            except Exception as e:
                print(
                    f"Error correcting time from config for {instrument.name}: {e}"
                )

    def data_corrections(
        self,
        start_altitude: float = None,
        start_pressure: float = None,
        start_temperature: float = None,
    ) -> None:
        success = []
        errors = []

        for instrument in self._instruments:
            try:
                instrument.df = instrument.data_corrections(
                    instrument.df,
                    start_altitude=start_altitude,
                    start_pressure=start_pressure,
                    start_temperature=start_temperature,
                )
                success.append(instrument.name)
            except Exception as e:
                errors.append((instrument.name, e))

        print(
            "Set pressure column for "
            f"({len(success)}/{len(self._instruments)}): {', '.join(success)}"
        )
        print(f"Errors ({len(errors)}/{len(self._instruments)}):")
        for error in errors:
            print(f"Error ({error[0]}): {error[1]}")

    def plot_pressure(self) -> None:
        """Creates a plot with the pressure measurement of each instrument

        Assumes the pressure column has been set for each instrument
        """

        fig, ax = plt.subplots()

        for instrument in self._instruments:
            # Check that the column exists
            if self.pressure_column not in instrument.df.columns:
                print(
                    f"Error: {instrument.name} does not have a pressure column"
                )
                continue
            ax.plot(
                instrument.df.index,
                instrument.df[self.pressure_column],
                label=instrument.name,
            )

        ax.set_title("Pressure measurements")
        ax.set_xlabel("Time")
        ax.set_ylabel("Pressure (hPa)")
        ax.legend()
        plt.show()
