import pika
import time
import pandas as pd
import ast
import json
from datetime import datetime, timedelta
# from celery import Celery


from common.constants import RABBITMQ_QUEUE_NAME, RABBITMQ_HOST, RABBITMQ_TRADE_QUEUE
from stratedy_db.strategy_db import GetStrategy
from strategy_builder.main import Strategy
from data_fetcher.data_fetcher import DataFetcher
from common.classes.option_chain import OptionChain

# app = Celery("tasks", broker="amqp://guest:guest@localhost//")

# class StrategyCaller:
#     def __init__(self, strategies_to_deploy=None):
#         strategy_list = list()
#         self.strategy_object_list = list()
#         if strategies_to_deploy:
#             for strategy in strategies_to_deploy:
#                 strategy_list.append(StrategyDB.find_strategy(strategy))
#
#             for strategy in strategy_list:
#                 self.strategy_object_list.append(Strategy(
#                     instrument_settings=strategy.get("instrument_settings"),
#                     legwise_settings=strategy.get("legwise_settings"),
#                     entry_settings=strategy.get("entry_settings"),
#                     legs=strategy.get("legs"),
#                     overall_strategy_settings=strategy.get("overall_strategy_settings")
#                 ))
#         self.message_publisher = MessageProducer()
#
#     def strategy_executer(self, ticker):
#         for strategy in self.strategy_object_list:
#             output = strategy.executor(ticker)
#             if output:
#                 self.message_publisher.publish(output)
#
#
# # Below class should be rabbitmq consumer (like a wrapper class) which should inherit a base class MessageConsumer
# class MessageConsumer:
#     def __init__(self):
#         self.queue_name = RABBITMQ_QUEUE_NAME
#
#         # Connection parameters
#         credentials = pika.PlainCredentials('guest', 'guest')
#         parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
#
#         # Establish connection
#         self.connection = pika.BlockingConnection(parameters)
#         self.channel = self.connection.channel()
#
#         # Declare the queue
#         self.channel.queue_declare(queue=self.queue_name)
#         self.strategy_caller = StrategyCaller(['1'])
#
#     def start_consuming(self):
#         # Set up a consumer and start consuming messages
#         self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
#         print(f'Waiting for messages on queue {self.queue_name}. To exit press CTRL+C')
#         self.channel.start_consuming()
#
#     def callback(self, ch, method, properties, body):
#         message = body.decode()
#
#         # convert message to dataframe
#         df = pd.DataFrame(json.loads(message))
#         df = ProcessData.process_data(df)
#         # Add your message processing logic here
#         self.strategy_caller.strategy_executer(df)
#
#     def close_connection(self):
#         # Close the connection
#         self.connection.close()
#
#
# class ProcessData:
#
#     @staticmethod
#     def process_data(data):
#         processed_data = data
#         processed_data["time"] = pd.to_datetime(processed_data['time'], format='%H:%M:%S').dt.time.iloc[0]
#         return processed_data


class MessageProducer:
    def __init__(self):
        self.queue_name = RABBITMQ_TRADE_QUEUE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()

        # # Declare the queue (this will create the queue if it doesn't exist)
        self.channel.queue_declare(queue=self.queue_name)

    def publish(self, data):
        try:
            json_data = json.dumps(data).encode('utf-8')
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json_data
            )
            print("Message published successfully")
        except Exception as e:
            print(f"Error publishing message: {e}")

    def close(self):
        self.connection.close()

# @app.task
def strategy_executor(strategy_id, index, execution_type, **kwargs):
    strategy = GetStrategy(strategy_id)
    # message_publisher = MessageProducer()
    if not strategy:
        raise ValueError("Could not find strategy in strategy DB")

    strategy_ob = Strategy(
                    instrument_settings=strategy.instrument_settings,
                    legwise_settings=strategy.legwise_settings,
                    entry_settings=strategy.entry_settings,
                    legs=strategy.legs,
                    overall_strategy_settings=strategy.overall_strategy_settings
                )
    if execution_type == "backtest":
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        current_date = start_date
        while current_date <= end_date:
            start_time = datetime.strptime('09:15', '%H:%M')
            end_time = datetime.strptime('15:30', '%H:%M')
            current_time = start_time
            while current_time <= end_time:
                option_chain = DataFetcher.fetch_data(index, date=current_date, time=str(current_time.time()))
                action = strategy_ob.executor(option_chain)
                if action:
                    print(action)
                current_time += timedelta(minutes=1)
            current_date += timedelta(days=1)


strategy_executor("1", "nifty", "backtest", start_date="2016-01-05", end_date="2016-01-05")
