from src.notify_service.config.celery import app
from src.notify_service.notify.providers.provider import SenderProvider


@app.task
def send_auth_message(data: dict):
    provider = SenderProvider.get_provider(data.pop("provider"))
    provider.send(data)
