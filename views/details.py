from views.utils import get_url

class View(dict):
    name = 'View'

    def __init__(self,request):
        self.request = request
        self['menu'] = self.get_menu()
        self['summary'] = self.get_summary()

    def get_menu(self):
        return {'title':'View','item_list':self.get_menu_item_list()}

    def get_menu_item_list(self):
        key = 'v'
        value = self.request.GET.get(key,'')
        item_list = [
            {'value':'100','text':'100'},
            {'value':'10','text':'10'},
            {'value':'1000','text':'1000'},
            {'value':'10000','text':'10000'},
        ]
        default_value = item_list[0]['value'] # todo: remake
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
