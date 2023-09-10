import os

from .conf import DJANGO_COMMAND_DIRNAME

def get_output_path(name,timestamp):
    return os.path.join(DJANGO_COMMAND_DIRNAME,name,str(timestamp))
