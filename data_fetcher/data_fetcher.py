from datetime import datetime, time
import pandas as pd
import os
import re

from common.constants import DATA_PATH
from common.classes.option_chain import OptionChain


class DataFetcher:

    @staticmethod
    def read_file(path):
        return pd.read_parquet(path)

    @staticmethod
    def fetch_data(index, date=None, latest=False, time=None):
        if date:
            date = str(date)
            path = os.path.join(DATA_PATH, index)
            if date:
                if os.path.exists(os.path.join(path, date)):
                    path = os.path.join(path, date)
                    if latest:
                        files = os.listdir(path)
                        parquet_files = [file for file in files if file.endswith('.parquet')]
                        timestamps = [re.search(r'\d{14}', file).group() for file in parquet_files]
                        timestamps = [pd.to_datetime(timestamp, format='%Y%m%d%H%M%S') for timestamp in timestamps]
                        parquet_files_sorted = [file for _, file in sorted(zip(timestamps, parquet_files))]
                        latest_file = parquet_files_sorted[-1]
                        data = DataFetcher.read_file(latest_file)
                        return data
                    elif time:
                        file = os.path.join(path, f"{time}.parquet")
                        if os.path.exists(file):
                            return DataFetcher.read_file(file)
                else:
                    file = os.path.join(path, f"{date}.parquet")
                    data = DataFetcher.read_file(file)
                    time_obj = datetime.strptime(time, "%H:%M:%S").time()
                    if time:
                        data = data[data["time"] == time_obj]
                    data = DataFetcher.process_backtest_data(data)
                    option_chain = OptionChain(data)
                    return option_chain

    @staticmethod
    def process_backtest_data(data):
        processed_data = data
        underlying_asset_price = {
            "ticker": "underlying_asset",
            "datetime": data[data["ticker"] == "NIFTY-I"].iloc[0]["datetime"],
            "date": data[data["ticker"] == "NIFTY-I"].iloc[0]["date"],
            "time": data[data["ticker"] == "NIFTY-I"].iloc[0]["time"],
            "open": data[data["ticker"] == "NIFTY-I"].iloc[0]["open"],
            "high": data[data["ticker"] == "NIFTY-I"].iloc[0]["high"],
            "low": data[data["ticker"] == "NIFTY-I"].iloc[0]["low"],
            "close": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
            "volume": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
            "open_interest": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
            "strike_price": None,
            "instrument_type": "cash",
            "expiry_date": None,
            "instrument_name": "underlying_asset",
            "expiry_type": None,
            "ltp": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
        }
        processed_data["ltp"] = processed_data["close"]
        processed_data["instrument_type"] = processed_data["instrument_type"].replace("PE", "put")
        processed_data["instrument_type"] = processed_data["instrument_type"].replace("CE", "call")
        processed_data = pd.DataFrame(processed_data.to_dict('records') + [underlying_asset_price])
        return processed_data
