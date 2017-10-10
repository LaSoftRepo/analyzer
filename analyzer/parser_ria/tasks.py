from celery import shared_task

from parser_ria.parser import ParserRia


@shared_task(name='parser-AUTO.RIA')
def start_parser_olx():
    parser = ParserRia()
    parser.start()