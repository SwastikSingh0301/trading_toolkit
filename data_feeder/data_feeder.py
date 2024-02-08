from data_feeder.backtester.back_tester import BackTester
import pika

from common.constants import RABBITMQ_QUEUE_NAME, RABBITMQ_HOST


# TODO: create a wrapper for rabbit mq and move all queue based code to that wrapper
# TODO: make this class a singelton
class RabbitMQ:
    def __init__(self):
        self.queue_name = RABBITMQ_QUEUE_NAME
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()

        # # Declare the queue (this will create the queue if it doesn't exist)
        # self.channel.queue_declare(queue=self.queue_name)

    def publish(self, data):
        json_data = data.to_json(orient='records')
        try:
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


class DataFeederFactory:
    @staticmethod
    def begin_data_feeding(type, meta_data):
        rabbitmq = RabbitMQ()
        if type == "backtest":
            start_date = meta_data["start_date"]
            end_date = meta_data["end_date"]
            index = meta_data["index"]
            data_feeder_object = BackTester(start_date, end_date, index)
        else:
            raise ValueError("Valid type not provided")     # Error message can be improved

        for each_data in data_feeder_object.begin_data_feeding_generator():
            rabbitmq.publish(each_data)
            break
        rabbitmq.close()

