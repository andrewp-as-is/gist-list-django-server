from views.details import Details

class Sort(Details):
    menu_title = 'Select order'
    menu_item_list = [
        # {'key':'stars','text':'Stars'},
        # {'key':'forks','text':'Forks'},
        {'value':'created','text':'Recently created'},
        {'value':'updated','text':'Recently updated'},
        {'value':'stars','text':'Most stars'},
        {'value':'forks','text':'Most forks'},
        {'value':'comments','text':'Most comments'},
        {'value':'-created','text':'Least recently created'},
        {'value':'-updated','text':'Least recently updated'},
        {'value':'name','text':'Name'},
        {'value':'description','text':'Description'},
        {'value':'id','text':'ID'},
    ]

class Type(Details):
    menu_title = 'Type'
    github_user = None

    def __init__(self,request,github_user):
        self.request = request
        self.github_user = github_user

    def get_menu_item_list(self):
        url = self.github_user.get_absolute_url()
        item_list = [
            {'value':'','text':'All','url':url,'selected':self.request.path.endswith(self.github_user.login)},
            {'value':'public','text':'Public','url':url+'/public','selected':self.request.path.endswith('/public')},
            {'value':'secret','text':'Secret','url':url+'/secret','selected':self.request.path.endswith('/secret')},
        ]
        return item_list
