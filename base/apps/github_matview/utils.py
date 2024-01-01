from django.apps import apps

MODEL_LIST = list(filter(
    lambda m:'github_matview' in m._meta.db_table,
    apps.get_models()
))
MATVIEW2MODEL = {m._meta.db_table.replace('"',''):m for m in MODEL_LIST}

def get_model(matviewname):
    return MATVIEW2MODEL[matviewname]
