import os, sys, time, traceback
from traceback import TracebackException

from .models import ExceptionModel


def save_exception(e):
    exception_type, exception_object, tb = sys.exc_info()
    exc_type = type(e).__name__
    exc_traceback = traceback.format_exc()
    timestamp = round(time.time(), 3)
    filename, lineno = tb.tb_frame.f_code.co_filename, tb.tb_lineno
    module = tb.tb_frame.f_globals["__name__"]
    for f in TracebackException.from_exception(e).stack:
        if os.getcwd() in f.filename:
            filename, lineno = f.filename, f.lineno
    defaults = dict(
        module=module,
        exc_type=exc_type,
        exc_message=str(e),
        exc_traceback=exc_traceback,
        timestamp=timestamp,
    )
    exc, created = ExceptionModel.objects.get_or_create(
        defaults, filename=filename, lineno=lineno
    )
