from views.details import Details

class Sort(Details):
    menu_title = 'Select order'
    menu_item_list = [
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
