from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from parser_olx.parser import ParserOlx
from parser_ria.parser import ParserRia
from sms_sender.sender import ClientSmsSender


def parse(r):
    parser = ParserOlx()
    parser.run()
    # parser = ClientSmsSender()
    return HttpResponse()