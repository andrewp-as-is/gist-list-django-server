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

    def get_url(self,**kwargs):
        data = {k:v for k,v in self.request.GET.items()}
        data.update(kwargs)
        params = []
        for k in list(filter(lambda k:k not in ['page'],data.keys())):
            params.append('%s=%s' % (k,data[k]))
        return self.request.path+'?'+'&'.join(params)

    def get_details_menu_item_list(self,key,item_list):
        request_value = self.request.GET.get(key,'')
        for item in item_list:
            # i['selected'] = item_value == value or item_text == value or (value=='' and item_value==default_value)
            # todo: item_text == value, item_text.lower() == value.lower()
            item['selected'] = item['value'] == request_value or item['description'] == request_value
            kwargs = {key:item['value']}
            if 'url' not in item:
                item['url'] = self.get_url(**kwargs)
        if not request_value:
            item_list[0]['selected'] = True
        return item_list


class PythonErrorMixin:
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            save_python_error(e)
            raise e
            #response = render(self.request,'500.html', status=500)
           # return response
