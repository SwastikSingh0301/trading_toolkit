import requests
import json
import pandas as pd
import numpy as np


def option_chain_data():
    new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(new_url, headers=headers)
    data = json.loads(page.text)
    data = data["records"]["data"]
    option_chain_df = pd.json_normalize(data)
    option_chain_df = process_data(option_chain_df)
    return option_chain_df

def process_data(df):
    ce_columns = [col for col in df.columns if col.startswith('CE.')]
    pe_columns = [col for col in df.columns if col.startswith('PE.')]

    # Create DataFrames for CE and PE
    df_ce = df[ce_columns].copy()
    df_pe = df[pe_columns].copy()

    # strike price
    df_pe["strike_price"] = df['PE.strikePrice'].astype(int)
    df_ce["strike_price"] = df['CE.strikePrice'].astype(int)

    # expiry_date
    df_pe.rename(columns={'PE.expiryDate': 'expiry_date'}, inplace=True)
    df_ce.rename(columns={'CE.expiryDate': 'expiry_date'}, inplace=True)
    df_pe["expiry_date"] = pd.to_datetime(df_pe['expiry_date']).dt.date
    df_ce["expiry_date"] = pd.to_datetime(df_ce['expiry_date']).dt.date

    # datetime, date, time
    current_time = pd.Timestamp.now()
    df_pe['datetime'] = current_time
    df_ce['datetime'] = current_time

    df_pe['date'] = current_time.date()
    df_ce['date'] = current_time.date()

    df_pe['time'] = current_time.time()
    df_ce['time'] = current_time.time()

    # close
    df_pe.rename(columns={'PE.lastPrice': 'close'}, inplace=True)
    df_ce.rename(columns={'CE.lastPrice': 'close'}, inplace=True)
    df_pe['ltp'] = df_pe['ltp'].replace(0, np.nan)
    df_ce['ltp'] = df_ce['ltp'].replace(0, np.nan)

    # volume
    df_pe.rename(columns={'PE.totalTradedVolume': 'volume'}, inplace=True)
    df_ce.rename(columns={'CE.totalTradedVolume': 'volume'}, inplace=True)

    # open_interest
    df_pe.rename(columns={'PE.openInterest': 'open_interest'}, inplace=True)
    df_ce.rename(columns={'CE.openInterest': 'open_interest'}, inplace=True)

    # instrument_type
    df_pe["instrument_type"] = "put"
    df_ce["instrument_type"] = "call"

    # ticker
    df_pe.rename(columns={'PE.identifier': 'ticker'}, inplace=True)
    df_ce.rename(columns={'CE.identifier': 'ticker'}, inplace=True)

    #underlying asset
    # underlying_asset_price = {
    #     "ticker": "underlying_asset",
    #     "datetime": current_time,
    #     "date": current_time.date,
    #     "time": current_time.time,
    #     "close": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
    #     "volume": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
    #     "open_interest": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
    #     "strike_price": None,
    #     "instrument_type": "cash",
    #     "expiry_date": None,
    #     "instrument_name": "underlying_asset",
    #     "expiry_type": None,
    #     "ltp": data[data["ticker"] == "NIFTY-I"].iloc[0]["close"],
    # }



option_chain_data()
