from django.db import models

SITE_LIST = (
    ('nyc', 'NYC'),
    ('bos', 'BOS'),
)

class SiteList(models.Model):
    site = models.CharField(max_length=3, choices=SITE_LIST)