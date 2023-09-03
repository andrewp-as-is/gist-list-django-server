from .models import Job

def create_job(name,priority=0):
    defaults = dict(priority=100)
    Job.objects.get_or_create(defaults,name=name)
