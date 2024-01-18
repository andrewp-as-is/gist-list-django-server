__all__ = ["UserApiEtagJob"]

from urllib.parse import parse_qs, urlparse

from django.db import models

def get_page(url):
    if "page" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["page"][0])


class UserApiEtagJob(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.OneToOneField('http_client.Response', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        page = get_page(response.url)
        return 'api.github.com' in response.url and (not page or page==1)
