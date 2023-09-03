import time

from .models import Cursor

def save_cursor(model,job_list):
    if job_list:
        job_id  = max(map(lambda j:j.id,job_list))
        defaults = dict(job_id=job_id,timestamp=int(time.time()))
        db_table = model._meta.db_table.replace('"','')
        regclass = '"%s"."%s"' % (
            db_table.split('.')[0],
            db_table.split('.')[1]
        )
        Cursor.objects.update_or_create(defaults,regclass=regclass)
