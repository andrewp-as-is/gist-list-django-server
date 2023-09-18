import time

from base.apps.http_response.management.base import ResponseJobCommand
from base.apps.http_etag.models import Etag
from base.utils import bulk_create, execute_sql


SQL = """
UPDATE http_etag.etag
SET timestamp=extract(epoch FROM (now()))
WHERE url IN (
    SELECT url
    FROM http_response.response
    WHERE id IN (
        SELECT response_id
        FROM http_etag.response_job
    ) and status=304
);
"""

class Command(ResponseJobCommand):

    def handle(self, *args, **options):
        self.create_list = []
        super().handle()
        bulk_create(self.create_list)
        execute_sql(SQL)

    def process_response(self,response):
        if response.status==200:
            headers = response.get_headers()
            etag = None
            for key,value in headers.items():
                if key.lower()=='etag':
                    etag = value
            if etag:
                self.create_list+=[Etag(
                    url = response.url,
                    etag = etag,
                    timestamp = int(time.time())
                )]
