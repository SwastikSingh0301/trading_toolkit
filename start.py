from data_feeder.data_feeder import DataFeederFactory


type = "backtest"
strategy = "1"
start_date = "2016-01-01"
end_date = "2016-01-01"
index = "nifty"



data = DataFeederFactory.begin_data_feeding(type=type, meta_data={
    "start_date": start_date,
    "end_date": end_date,
    "index": index
})

