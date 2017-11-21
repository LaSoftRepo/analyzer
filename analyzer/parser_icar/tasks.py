from celery import shared_task

from parser_icar.parser import ParserIcar
from settings_analyzer.models import StatusSiteParse


@shared_task(name='parser-ICAR')
def start_parser_icar():
    site = StatusSiteParse.objects.filter(name__exact='avtobazar.infocar.ua')
    if site.exists():
        site = site.first()
        if site.is_enable:
            parser = ParserIcar()
            parser.start()
