import io
import os
from uuid import uuid4
from PIL import Image

from django.utils.deconstruct import deconstructible


@deconstructible
class FilePath(object):
    def __init__(self, sub_path, custom_name=None):
        self.path = sub_path
        self.custom_name = custom_name

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(self.custom_name if self.custom_name else uuid4().hex, ext)
        return os.path.join(self.path.format(**instance.__dict__), filename)


def file_path(folder, custom_name=''):
    return FilePath(os.path.join(folder, custom_name))


def test_file(name='test.png', extension='png'):
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, extension)
    file.name = name
    file.seek(0)
    return file


def get_files_for_checking(start_path):
    source_files = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        for file in files:
            if file.endswith('.py') and not root.endswith('migrations') and 'chat' not in root:
                source_files.append('%s/%s' % (root, file))
    return source_files


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
