import datetime
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.TextField()


class Image(models.Model):
    name = models.CharField(max_length=255)
    related = models.ForeignKey('Post')
    date = models.DateTimeField(default=datetime.datetime.now)
    file = models.ImageField(upload_to="images/")

    def __unicode__(self):
        return self.name
