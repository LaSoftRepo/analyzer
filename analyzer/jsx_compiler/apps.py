from django.apps import AppConfig
from django.conf import settings

from jsx_compiler.compiler import JsxCompiler


class JsxCompilerConfig(AppConfig):
    name = 'jsx_compiler'
    def ready(self):
        auto_compile = settings.JSX_COMPILER.get('AUTO_COMPILE') or True
        if auto_compile:
            JsxCompiler().compile()