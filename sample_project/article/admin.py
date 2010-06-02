from django.contrib import admin
from sample_project.article.models import Post, Image
from sample_project.article.forms import ImageForm, PostAdminModelForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminModelForm
    class Media:
        css = {
            "all": ("css/overlay.css",)
        }
        js = ("js/jquery-1.4.2.min.js",
              "js/jquery.tools.min.js",
              "js/file-picker.js",
              "js/plupload.full.min.js",
        )
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)
