from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from jsx_compiler.compiler import JsxCompiler

register = template.Library()

@register.simple_tag(name='compiled_js')
def compiled_js():
    files = JsxCompiler().get_compiled_files()
    paths = []
    if files:
        for file in files:
            path = f'<script type="text/javascript" src="{settings.STATIC_URL}js/src/{file}"></script>'  # noqa
            paths.append(path)

    return mark_safe(''.join(paths))
