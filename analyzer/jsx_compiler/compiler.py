import os

from django.conf import settings


class JsxCompiler:

    def __init__(self):
        self.src_path = self._get_src_path
        self.tmp_path = self._get_tmp_path
        self.suffix = '.js'
        self.end_line = '+'

    @property
    def _get_src_path(self):
        return settings.JSX_COMPILER.get('SRC_PATH') \
               or os.path.join(settings.BASE_DIR, 'static/js/src')

    @property
    def _get_tmp_path(self):
        try:
            return settings.JSX_COMPILER['TMP_PATH']
        except KeyError:
            raise KeyError('TMP_PATH key must be defined in JSX_COMPILER')

    def get_compiled_files(self):
        return os.listdir(self.src_path)

    def compile(self):
        files = os.listdir(self.tmp_path)
        for file in files:
            if file.endswith('jsx'):
                file_path = '/'.join((self.tmp_path, file))
                js_file_path = self._create_file(file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    self._transform_jsx_to_js(lines, js_file_path)

    def _transform_jsx_to_js(self, lines, js_file_path):
        for i, line in enumerate(lines):
            line = line.replace('\n', '')
            if 'var' not in line:
                if line:
                    if ';' == line[-1]:
                        line = line.replace(';', '')
                        self.end_line = ';'
                    line = ''.join(('\'', line, '\'', self.end_line, '\n'))
                    self.end_line = '+'
            else:
                line = ''.join((line, '\n'))

            self._save_file(line, js_file_path)

    def _save_file(self, line, path):
        with open(path, 'a') as f:
            f.writelines(line)

    def _create_file(self, name):
        name = name.split('.')[0] + self.suffix
        path = '/'.join((self.src_path, name))
        try:
            with open(path, 'w') as f:
                pass
        except FileNotFoundError:
            os.mkdir(self.src_path)
        return path