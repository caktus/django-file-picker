from django.db import models
from django.contrib import admin
from sample_project.blog.models import Post, Image, File
from sample_project.blog.forms import PostAdminModelForm

import file_picker

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': file_picker.widgets.WYMeditorWidget(pickers={
                'file': 'blog-file',
                'image': 'blog-image',
            })
        },
    }
    class Media:
        css = {
            "all": (
                    "css/overlay.css",
                   )
        }
        js = ("js/jquery-1.4.2.min.js", "js/jquery.tools.min.js",
              "wymeditor/jquery.wymeditor.pack.js",
              "js/file-picker.js", "js/file-picker-wymeditor.js", 
              "js/ajaxupload.js",)
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)

class FileAdmin(admin.ModelAdmin):
    pass
admin.site.register(File, FileAdmin)
