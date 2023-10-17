import os, sys, time, traceback

from .models import PythonError

def save_python_error(e):
    # exc_type, exc_obj, exc_tb = sys.exc_info()
    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    PythonError(
        filename='todo',
        exc_type=type(e),
        exc_message=str(e),
        exc_traceback=traceback.format_exc(),
        timestamp=int(time.time())
    ).save()
