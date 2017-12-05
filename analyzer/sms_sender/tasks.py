from celery import shared_task

from sms_sender.sender import ClientSmsSender


@shared_task(name='Sender SMS')
def start_sender_sms():
    print('Start SENDER SMS')
    send = ClientSmsSender()
    send.start()
