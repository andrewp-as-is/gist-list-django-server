

class Details(dict):
    key = None # ?key=value
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
            'item_list':self.get_menu_item_list()
        }

    def get_default_value(self):
        if self.default_value:
            return self.default_value
        return self.menu_item_list[0]['value']

    def get_key(self):
        return (self.key or type(self).__name__).lower()

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

    def __bool__(self):
        return len(self.get_menu_item_list())>0


class View(Details):
    key = 'v'
    default_value = '50'
    menu_item_list = [
        {'value':'10','text':'10'},
        {'value':'20','text':'20'},
        {'value':'50','text':'50'},
        {'value':'100','text':'100'},
        {'value':'1000','text':'1000'},
    ]
