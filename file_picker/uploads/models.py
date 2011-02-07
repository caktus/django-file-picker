import os
import datetime

from django.db import models
from django.contrib.auth.models import User


class BaseFileModel(models.Model):
    """ Base file model with meta fields """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=16, blank=True)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created",
                                   null=True, blank=True)
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified",
                                    null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-date_modified',)

    def save(self, **kwargs):
        # dates
        now = datetime.datetime.now()
        if not self.pk:
            self.date_created = now
        self.date_modified = now
        # file info
        try:
            self.file_size = self.file.size
        except OSError:
            pass
        path, ext = os.path.splitext(self.file.name)
        self.file_type = ext.lstrip('.').upper()
        return super(BaseFileModel, self).save(**kwargs)

    def __unicode__(self):
        return self.name


class File(BaseFileModel):
    """ Basic file field model """
    file = models.FileField(upload_to='uploads/files/')


class Image(BaseFileModel):
    """ Basic image field model """
    file = models.ImageField(upload_to='uploads/images/')

