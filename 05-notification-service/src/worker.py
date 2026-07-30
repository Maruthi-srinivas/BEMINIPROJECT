"""RabbitMQ consumer for the notification service."""

from __future__ import annotations

import asyncio
import json
import logging
import os

import aio_pika

from src.main import DLQ_NAME, QUEUE_NAME, SessionLocal, Notification, process_notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification_worker")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")


async def main() -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    await channel.declare_queue(DLQ_NAME, durable=True)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    exchange = channel.default_exchange
    logger.info("listening on %s", QUEUE_NAME)

    async def on_message(message: aio_pika.IncomingMessage) -> None:
        async with message.process(requeue=False):
            notification_id = int(json.loads(message.body.decode())["id"])
            process_notification(notification_id)
            with SessionLocal() as db:
                row = db.get(Notification, notification_id)
                if not row:
                    return
                if row.status == "queued":
                    delay = min(2 ** row.attempts, 60)
                    await asyncio.sleep(delay)
                    await exchange.publish(
                        aio_pika.Message(
                            body=message.body,
                            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                        ),
                        routing_key=QUEUE_NAME,
                    )
                elif row.status == "dead":
                    await exchange.publish(
                        aio_pika.Message(
                            body=message.body,
                            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                        ),
                        routing_key=DLQ_NAME,
                    )

    await queue.consume(on_message)
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
