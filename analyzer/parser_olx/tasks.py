from celery import shared_task

from parser_olx.parser import ParserOlx
from settings_analyzer.models import StatusSiteParse


@shared_task(name='parser-OLX')
def start_parser_olx():
    site = StatusSiteParse.objects.filter(name__exact='olx.ua')
    if site.exists():
        site = site.first()
        if site.is_enable:
            parser = ParserOlx()
            parser.run()
