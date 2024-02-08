from datetime import datetime
import pandas as pd
import os

from common.constants import INDEX, NIFTY_HISTORICAL_DATA, BANKNIFTY_HISTORICAL_DATA


class BackTester:
    def __init__(self, start_date, end_date, index):
        self.start_date = self.process_date(start_date)
        self.end_date = self.process_date(end_date)
        self.index = index

    def read_parquet(self, folder_path):
        parquet_files = [file for file in os.listdir(folder_path) if file.endswith('.parquet')]
        dfs = []  # List to store DataFrames from each file
        for file_name in parquet_files:
            file_date_str = file_name.split(".")[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")

            # Check if the file date is within the specified range
            if self.start_date <= file_date <= self.end_date:
                file_path = os.path.join(folder_path, file_name)

                # Read the Parquet file and convert to a pandas DataFrame
                df = pd.read_parquet(file_path)
                # Append the DataFrame to the list
                dfs.append(df)


        # Concatenate all DataFrames into a single DataFrame
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df

    def get_index_path(self, index):
        if index == INDEX.NIFTY:
            path = NIFTY_HISTORICAL_DATA
        elif index == INDEX.BANKNIFTY:
            path = BANKNIFTY_HISTORICAL_DATA
        else:
            raise ValueError("wrong index")
            pass
        return path

    # def process_data(self, data):
    #     data = data.sort_values(by='date')
    #     grouped_by_date = data.groupby("date")
    #     for date, date_group in grouped_by_date:
    #         date_group = date_group.sort_values(by="time")
    #         time_group = date_group.groupby("time")


    def process_date(self, date_string):
        date_format = "%Y-%m-%d"

        # Convert the string to a datetime object
        date = datetime.strptime(date_string, date_format)
        return date

    def begin_data_feeding_generator(self):
        path_to_historical_data = self.get_index_path(self.index)
        historical_data = self.read_parquet(path_to_historical_data)
        data = historical_data.sort_values(by='date')
        grouped_by_date = data.groupby("date")
        for date, date_group in grouped_by_date:
            date_group = date_group.sort_values(by="time")
            grouped_by_time = date_group.groupby("time")
            for time, time_group in grouped_by_time:
                yield time_group

