from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from parser_icar.parser import ParserIcar
from parser_olx.parser import ParserOlx
from parser_rst.parser import ParserRst
from parser_ria.parser import ParserRia
from sms_sender.sender import ClientSmsSender


def parse(r):
    # parser = ParserRst()
    # parser.start()
    # parser = ClientSmsSender()

    # parser = ParserRia()
    # parser.start()

    parser = ParserIcar()
    parser.start()
    return HttpResponse()