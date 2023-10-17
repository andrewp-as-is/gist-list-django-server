import time

from .models import Cursor

# TODO: REGCLASS2CURSOR_ID

def save_cursor(model,job_id):
    db_table = model._meta.db_table.replace('"','')
    schemaname = db_table.split('.')[0].replace('"','')
    viewname = db_table.split('.')[1].replace('"','')
    cursor = Cursor.objects.get(schemaname=schemaname,viewname=viewname) # make sure cursor exists
    Cursor.objects.filter(id=cursor.id).update(
        job_id=job_id,
        timestamp=int(time.time())
    )
