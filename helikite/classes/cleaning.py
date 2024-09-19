import pandas as pd
from typing import Any
import datetime
from helikite.instruments.base import Instrument
from helikite.constants import constants


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

        # Create an attribute from each instrument.name
        for instrument in instruments:
            instrument.df_original = instrument.read_from_folder(
                input_folder, quiet=True
            )
            instrument.df = instrument.df_original.copy(deep=True)
            instrument.date = flight_date

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
        from_column_override: str = None,
        column_name: str = constants.HOUSEKEEPING_VAR_PRESSURE,
    ) -> None:
        for instrument in self._instruments:
            try:
                instrument.df = (
                    instrument.set_housekeeping_pressure_offset_variable(
                        instrument.df, column_name
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

        print(trim_start, trim_end)
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
        for instrument in self._instruments:
            try:
                instrument.df = instrument.data_corrections(
                    instrument.df,
                    start_altitude=start_altitude,
                    start_pressure=start_pressure,
                    start_temperature=start_temperature,
                )
                print("Applied data corrections for", instrument.name)
            except Exception as e:
                print(
                    f"Error applying data corrections for {instrument.name}: {e}"
                )
