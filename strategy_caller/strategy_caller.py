import pika

from common.constants import RABBITMQ_QUEUE_NAME, RABBITMQ_HOST


# Below class should be rabbitmq consumer (like a wrapper class) which should inherit a base class MessageConsumer
class MessageConsumer:
    def __init__(self):
        self.queue_name = RABBITMQ_QUEUE_NAME

        # Connection parameters
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

        # Establish connection
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=self.queue_name)

    def start_consuming(self):
        # Set up a consumer and start consuming messages
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(f'Waiting for messages on queue {self.queue_name}. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print("Received message:", body.decode())
        message = body.decode()
        # Add your message processing logic here

    def close_connection(self):
        # Close the connection
        self.connection.close()


class StrategyCaller:
    def __init__(self, strategies=None):
        pass
        for strategy in strategies:
            strategy


    def consume(self):
        pass
