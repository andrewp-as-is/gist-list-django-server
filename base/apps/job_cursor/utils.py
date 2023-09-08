import time

from .models import Cursor

def save_cursor(name,job_list):
    if job_list:
        row_id  = max(map(lambda j:j.id,job_list))
        cursor = Cursor.objects.get(name=name) # make sure name exists
        Cursor.objects.filter(id=cursor.id).update(
            row_id=row_id,timestamp=int(time.time())
        )
