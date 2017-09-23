from django.shortcuts import render

# Create your views here.
from parser_olx.parser import ParserOlx


def parse(r):
    parser = ParserOlx()
    parser.run()