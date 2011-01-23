from django.contrib import admin
from django.db import models
from sample_project.article.models import Post

import file_picker


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': file_picker.widgets.FilePickerWidget(pickers={
                'image': "images",
                'file': "files",
            }),
        },
    }

    class Media:
        css = {"all": ("css/filepicker.overlay.css",)}
        js = ("https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js",
              "http://cdn.jquerytools.org/1.2.2/tiny/jquery.tools.min.js",
              "js/overlay.apple.min.js",
              "js/ajaxupload.js",
              "js/jquery.filepicker.js",
              "js/jquery.filepicker.simple.js",)

admin.site.register(Post, PostAdmin)

