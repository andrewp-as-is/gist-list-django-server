import os
import traceback
from traceback import TracebackException


def func2():
    eetetet

def func():
    func2()

try:
    func()
except Exception as e:
    tbe = TracebackException.from_exception(e)
    DIRNAME = os.path.dirname(__file__)
    for frame_summary in tbe.stack:
        summary_details = {
            'filename': frame_summary.filename,
            'method'  : frame_summary.name,
            'lineno'  : frame_summary.lineno,
            'code'    : frame_summary.line
        }
        print(summary_details)
        # error_lines.append(summary_details)
