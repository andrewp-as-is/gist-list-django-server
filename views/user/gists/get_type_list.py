    def get_type_list(self):
        value = self.request.GET.get('type','')
        default_value = ''
        item_list = [{'key':'','name':'All','count':''},]
        if self.request.user.is_authenticated and self.github_user.login==self.request.user.login:
            if self.github_user.public_gists_count and self.github_user.private_gists_count:
                item_list+= [
                    {'key':'public','name':'Public','count':self.github_user.public_gists_count}
                ]
            if self.github_user.private_gists_count:
                item_list+= [
                    {'key':'private','name':'Private','count':self.github_user.private_gists_count},
                ]
        for i in item_list:
            i['selected'] = i['key'] == value or (value=='' and i['key']==default_value)
            i['url'] = self.get_url(type=i['key'])
        return item_list
