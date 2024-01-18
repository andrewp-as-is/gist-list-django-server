import time

from django.db import connection
from django.shortcuts import render

#from base.apps.error.models import PythonError
#from base.apps.error.utils import save_python_error
#from base.apps.incident.models import Incident
from base.apps.postgres.models import Query

class Mixin:

    def execute_sql(self, query):
        cursor = connection.cursor()
        created_at = time.time()
        cursor.execute(query)
        duration = round(time.time()-created_at,3)
        Query(query=query,duration=duration,created_at=int(created_at)).save()



class PythonErrorMixin:
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            save_python_error(e)
            raise e
            #response = render(self.request,'500.html', status=500)
           # return response
