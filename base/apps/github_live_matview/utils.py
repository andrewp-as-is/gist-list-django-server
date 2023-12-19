
def iter_app_model_list(app_label):
    for model in apps.get_models():
        if model._meta.app_label==app_label:
            yield model
