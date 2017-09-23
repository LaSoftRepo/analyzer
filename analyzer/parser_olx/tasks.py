from celery import shared_task

from parser_olx.parser import ParserOlx


@shared_task(name='parser-OLX')
def start_parser_olx():
    parser = ParserOlx()
    parser.run()
