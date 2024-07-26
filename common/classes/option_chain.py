import pandas as pd
import json

from .option import Option


class OptionChain:
    def __init__(self, df):
        self.option_chain = df

    @property
    def time(self):
        try:
            # if time is in string then convert it to time object here
            return self.option_chain.iloc[0].time
        except:
            return None

    @property
    def full_option_chain(self):
        return self.option_chain

    # @property
    # def symbol(self):
    #     return

    @property
    def underlying_asset_price(self):
        return self.option_chain[self.option_chain["ticker"] == "underlying_asset"].iloc[0]["close"]

    def get_option(self, strike_price, option_type):
        if strike_price and option_type:
            option = self.option_chain[
                (self.option_chain["strike_price"] == strike_price) &
                (self.option_chain["instrument_type"] == option_type)
                ]
            if option.shape[0] > 1:
                """ Got more than 1 row with provided option type and strike price"""
                print(f"ERROR: Got more than 1 row with {option_type} option type and  {strike_price} strike price")
                return None
            if option.shape[0] < 1:
                """ Got 0 rows with provided option type and strike price"""
                print(f"ERROR: Got 0 rows with {option_type} option type and  {strike_price} strike price")
                return None
            option_json = option.iloc[0].to_json()
            option = Option(json.loads(option_json))
            return option

        return None

