from views.details import View
from views.utils import get_url

class Sort(dict):
    name = 'Sort'

    def __init__(self,request):
        self.request = request
        self['menu'] = self.get_menu()
        self['summary'] = self.get_summary()

    def get_menu(self):
        return {'title':'Sort','item_list':self.get_menu_item_list()}

    def get_menu_item_list(self):
        key = 'sort'
        value = self.request.GET.get(key,'')
        item_list = [
            # {'key':'stars','text':'Stars'},
            # {'key':'forks','text':'Forks'},
            {'value':'created','text':'Recently created'},
            {'value':'-created','text':'Least recently created'},
            {'value':'updated','text':'Recently updated'},
            {'value':'-updated','text':'Least recently updated'},
            {'value':'id','text':'ID'},
            {'value':'name','text':'Name'},
            {'value':'description','text':'Description'},
            {'value':'stars','text':'Most stars'},
            {'value':'forks','text':'Most forks'},
            {'value':'comments','text':'Most comments'},
        ]
        default_value = item_list[0]['value']
        for i in item_list:
            i['selected'] = i['value'] == value or (value=='' and i['value']==default_value)
            kwargs = {key:i['value']}
            i['url'] = get_url(self.request,**kwargs)
        return item_list

    def get_summary(self):
        text = self.get_menu_item_list()[0]['text']
        for item in self.get_menu_item_list():
            if item['selected']:
                text = item['text']
        return {'name':self.name,'text':text}
