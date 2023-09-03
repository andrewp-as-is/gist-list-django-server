import time, traceback

from django.db.models import F
from .models import PythonError

def save_python_error(e):
    defaults = dict(
        exc_type=type(e).__name__,
        exc_message=str(e),
        exc_traceback=traceback.format_exc(),
        timestamp=int(time.time())
    )
    filename = e.__traceback__.tb_frame.f_code.co_filename
    lineno = e.__traceback__.tb_lineno
    error,created = PythonError.objects.get_or_create(defaults,
        filename=filename,
        lineno=lineno
    )
    if not created:
        PythonError.objects.filter(id=error.id).update(
            count = error.count+1,
            timestamp=int(time.time())
        )
