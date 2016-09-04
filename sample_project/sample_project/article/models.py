import datetime
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.TextField()
    teaser = models.TextField()
