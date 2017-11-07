from celery import shared_task

from parser_ria.parser import ParserRia
from settings_analyzer.models import StatusSiteParse


@shared_task(name='parser-AUTO-RIA')
def start_parser_ria():
    site = StatusSiteParse.objects.filter(name__exact='auto.ria.com')
    if site.exists():
        site = site.first()
        if site.is_enable:
            parser = ParserRia()
            parser.start()