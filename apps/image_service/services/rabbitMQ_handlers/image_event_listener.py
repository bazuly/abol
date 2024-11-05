import pika
import json
import logging
import time

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    message = json.loads(body)
    logger.info(f"Received message: {message}")
    print(f"Received message: {message}")


time.sleep(10)


def listen_for_events():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq',
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        ))
        channel = connection.channel()
        logger.info("Connected to RabbitMQ")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")

    channel.queue_declare(queue='image_events')

    channel.basic_consume(
        queue='image_events',
        on_message_callback=callback,
        auto_ack=True
    )

    print('Listening for image events...')
    channel.start_consuming()


if __name__ == "__main__":
    listen_for_events()
