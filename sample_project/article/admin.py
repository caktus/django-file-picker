from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse

from sample_project.article.models import Post, Image

import file_picker


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': file_picker.widgets.BasicFilePickerWidget(picker="article")
        },
    }

    class Media:
        css = {"all": ("css/overlay.css",)}
        js = ("js/jquery-1.4.2.min.js",
              "js/jquery.tools.min.js",
              "js/ajaxupload.js",
              "js/file-picker.js",)

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
