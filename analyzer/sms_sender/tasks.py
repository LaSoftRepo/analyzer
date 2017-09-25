from celery import shared_task

from sms_sender.sender import ClientSmsSender


@shared_task(name='Sender SMS')
def start_sender_sms():
    send = ClientSmsSender()
    send.start()