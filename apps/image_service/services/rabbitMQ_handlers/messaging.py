import pika
import json
import logging

# Инициализация логгера
logger = logging.getLogger(__name__)


def publish_message(event_type, image_id, description=""):
    """
    Публикация сообщений в RabbitMQ.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Создание очереди, если её ещё нет
    channel.queue_declare(queue='image_events')

    message = {
        'event_type': event_type,
        'image_id': image_id,
        'description': description,
    }

    # Публикация сообщения
    channel.basic_publish(
        exchange='',
        routing_key='image_events',
        body=json.dumps(message)
    )

    logger.info(f"Sent {event_type} message for image {image_id}")
    connection.close()
