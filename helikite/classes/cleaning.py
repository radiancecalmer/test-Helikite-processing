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
        self.master_df: pd.DataFrame | None = None
        self.housekeeping_df: pd.DataFrame | None = None

        # Create an attribute from each instrument.name
        for instrument in instruments:
            instrument.df_raw = instrument.read_from_folder(
                input_folder, quiet=True
            )
            instrument.df = instrument.df_raw.copy(deep=True)
            instrument.date = flight_date
            instrument.time_offset = {}
            instrument.time_offset["hour"] = time_offset.hour
            instrument.time_offset["minute"] = time_offset.minute
            instrument.time_offset["second"] = time_offset.second

            # Add the instrument to the Cleaner object and the list
            setattr(self, instrument.name, instrument)
            self._instruments.append(instrument)

        self.print_instruments()
        print(
            "Helikite Cleaner has been initialised. Each instrument has "
            "been assigned a df attribute where processing changes will ",
            "occur, and an untouched df_raw. For example: "
            "Cleaner.flight_computer.df",
        )

    def print_instruments(self) -> None:
        for instrument in self._instruments:
            print(f"Cleaner.{instrument.name} ({len(instrument.df)} records)")

    def set_pressure_column(
        self,
        column_name: str = constants.HOUSEKEEPING_VAR_PRESSURE,
    ) -> None:

        success = []
        errors = []
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
                success.append(instrument.name)
            except Exception as e:
                errors.append((instrument.name, e))

        self.print_success_errors("pressure column", success, errors)

    def set_time_as_index(self) -> None:
        success = []
        errors = []

        for instrument in self._instruments:
            try:
                instrument.df = instrument.set_time_as_index(instrument.df)
                success.append(instrument.name)
            except Exception as e:
                errors.append((instrument.name, e))

        self.print_success_errors("time as index", success, errors)

    def correct_time(
        self,
        trim_start: pd.Timestamp | None = None,
        trim_end: pd.Timestamp | None = None,
    ) -> None:

        success = []
        errors = []

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
                success.append(instrument.name)
            except Exception as e:
                errors.append((instrument.name, e))

        self.print_success_errors("time corrections", success, errors)

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

        self.print_success_errors("data corrections", success, errors)

    def plot_pressure(self) -> None:
        """Creates a plot with the pressure measurement of each instrument

        Assumes the pressure column has been set for each instrument
        """

        fig, ax = plt.subplots()

        for instrument in self._instruments:
            # Check that the column exists
            if self.pressure_column not in instrument.df.columns:
                print(
                    f"Note: {instrument.name} does not have a pressure column"
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

    def remove_duplicates(self) -> None:

        success = []
        errors = []
        for instrument in self._instruments:
            try:
                instrument.df = instrument.remove_duplicates(instrument.df)
                success.append(instrument.name)
            except Exception as e:
                errors.append((instrument.name, e))

        self.print_success_errors("duplicate removal", success, errors)

    def print_success_errors(
        self,
        operation: str,
        success: list[str],
        errors: list[tuple[str, Any]],
    ) -> None:
        print(
            f"Set {operation} for "
            f"({len(success)}/{len(self._instruments)}): {', '.join(success)}"
        )
        print(f"Errors ({len(errors)}/{len(self._instruments)}):")
        for error in errors:
            print(f"Error ({error[0]}): {error[1]}")

    def merge_instruments(self):
        """Merges all of the dataframes from the instruments and exports them

        The dataframes are merged based on the DateTime index. The order of the
        columns is determined by the export_order attribute of the Instrument
        objects. If this attribute does not exist, the columns are placed at
        the end of the dataframe.
        """
        for instrument in self._instruments:
            instrument.df = instrument.add_device_name_to_columns(
                instrument.df
            )

        print(
            "Added instrument names to columns in their respective dataframes."
        )

        # Sort the export columns in their numerical hierarchy order and log
        self._instruments.sort(key=lambda x: x.export_order)
        print("Instruments will be merged together with this column order:")
        for instrument in self._instruments:
            for column in instrument.export_columns:
                print(column)

        # Merge all the dataframes together, first df is the master
        self.master_df = self._instruments[0].df
        for instrument in self._instruments[1:]:
            self.master_df = self.master_df.merge(
                instrument.df,
                how="outer",
                left_index=True,
                right_index=True,
            )

        # Sort rows by the date index
        self.master_df.index = pd.to_datetime(self.master_df.index)
        self.master_df.sort_index(inplace=True)

        print("The master dataframe has been created at Cleaner.master_df.")

    def export_data(
        self,
        master_filename: str = "master.csv",
        housekeeping_filename: str = "housekeeping.csv",
        export_master: bool = True,
        export_housekeeping: bool = True,
    ) -> None:
        """Export the merged dataframes to CSV files"""

        # Raise error if the dataframes have not been merged
        if hasattr(self, "master_df") is False or self.master_df.empty:
            raise ValueError(
                "Dataframes have not been merged. Please run the "
                "merge_instruments() method."
            )

        # Export data and housekeeping CSV files using the column names from
        # the instruments
        if export_master:
            master_cols = [
                f"{col}"
                for instrument in self._instruments
                for col in instrument.export_columns
            ]
            self.master_df[master_cols].to_csv(master_filename)

        if export_housekeeping:
            housekeeping_cols = [
                f"{col}"
                for instrument in self._instruments
                for col in instrument.housekeeping_columns
            ]
            self.master_df[housekeeping_cols].to_csv(housekeeping_filename)

        print("\nDone.")
        print("\tDataframes have been exported to CSV files.")

        if export_master:
            print(f"\tThe file '{master_filename}' contains the data columns")
        if export_housekeeping:
            print(
                f"\tThe file '{housekeeping_filename}' contains the "
                "housekeeping columns."
            )
        print(
            "\tThe column order is determined by the export_order attribute."
        )
        print(
            "\tThe order of the instruments is determined by the export "
            "order defined in each instrument's class."
        )
