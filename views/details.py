

class Details(dict):
    name = None # summary name
    key = None # ?key=value
    summary_css_class = None
    menu_title = None
    default_value = None
    menu_item_list = []

    def __init__(self,request,**kwargs):
        self.request = request
        for k,v in kwargs.items():
            setattr(self,k,v)

    def get_url(self,**kwargs):
        data = {k:v for k,v in self.request.GET.items()}
        data.update(kwargs)
        params = []
        for k in list(filter(lambda k:k not in ['page'],data.keys())):
            params.append('%s=%s' % (k,data[k]))
        return self.request.path+'?'+'&'.join(params)

    def get_menu(self):
        return {
            'title':self.menu_title or self.name or type(self).__name__,
            'item_list':self.get_menu_item_list()
        }

    def get_default_value(self):
        if self.default_value:
            return self.default_value
        return self.menu_item_list[0]['value']

    def get_key(self):
        return (self.key or self.name or type(self).__name__).lower()

    def get_menu_item_list(self):
        key = self.get_key()
        value = self.request.GET.get(key,'')
        default_value = self.get_default_value()
        item_list = []
        for i in self.menu_item_list:
            i['selected'] = i['value'] == value or i['text'] == value or (value=='' and i['value']==default_value)
            kwargs = {key:i['value']}
            if 'url' not in i:
                i['url'] = self.get_url(**kwargs)
            item_list+=[i]
        return item_list

    def get_values(self):
        return list(map(lambda i:i['value'],self.get_menu_item_list()))

    def get_summary(self):
        key = self.get_key()
        text = ''
        if self.request.GET.get(key,''):
            text = self.get_menu_item_list()[0]['text']
        for item in self.get_menu_item_list():
            if item['selected'] and self.request.GET.get(key,''):
                text = item['text']
        return {
            'name':self.name or type(self).__name__,
            'text':text,
            'css_class':self.summary_css_class
        }


class View(Details):
    key = 'v'
    default_value = '50'
    menu_title = 'Results per page'
    menu_item_list = [
        {'value':'10','text':'10'},
        {'value':'20','text':'20'},
        {'value':'50','text':'50'},
        {'value':'100','text':'100'},
        {'value':'1000','text':'1000'},
    ]
