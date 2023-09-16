import os, sys, time, traceback
from traceback import TracebackException

from django.db.models import F
from .models import PythonError

def save_python_error(e):
    exception_type, exception_object, tb = sys.exc_info()
    code_dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    filename, lineno = tb.tb_frame.f_code.co_filename, tb.tb_lineno
    print('code_dirname: %s' % code_dirname)
    for f in TracebackException.from_exception(e).stack:
        if code_dirname in f.filename:
            filename, lineno = f.filename, f.lineno
    defaults = dict(
        exc_type=type(e).__name__,
        exc_message=str(e),
        exc_traceback=traceback.format_exc(),
        timestamp=int(time.time())
    )
    error,created = PythonError.objects.get_or_create(defaults,
        filename=filename,
        lineno=lineno
    )
    if not created:
        PythonError.objects.filter(id=error.id).update(
            count = error.count+1,
            exc_type=type(e).__name__,
            exc_message=str(e),
            exc_traceback=traceback.format_exc(),
            timestamp=int(time.time())
        )
