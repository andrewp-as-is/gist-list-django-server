from management.base import JobCommand
from ...models import Etag

MODEL2BULK_CREATE_KWARGS = {
    Etag:dict(
        update_conflicts=True,
        unique_fields=["url"],
        update_fields=[
            "etag",
        ]
    )
}


class Command(JobCommand):
    MODEL2BULK_CREATE_KWARGS = MODEL2BULK_CREATE_KWARGS

    def do_job(self,job):
        response = job.response
        if response.status!=200:
            raise ValueError('%s %s' % (response.url,response.status))
        if '&etag=' in response.url:
            headers = response.get_headers()
            if 'Etag' in headers:
                etag = headers['Etag']
                self.create(Etag(url=response.url,etag=etag))
