from .models import Job

def create_job(name,priority=None):
    defaults = dict(priority=priority if priority else 0)
    print('CREATE: django_command_job.job with name="%s"' % name)
    Job.objects.get_or_create(defaults,name=name)
