# Используем базовый образ
FROM abol-base

WORKDIR /app

COPY ./apps/image_service /app/apps/image_service

WORKDIR /app/apps/image_service/services/rabbitMQ_handlers

CMD ["python", "image_event_listener.py"]
