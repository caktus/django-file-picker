from django.contrib import admin
from sample_project.blog.models import Post, Image
from sample_project.blog.forms import ImageForm, PostAdminModelForm, PageletForm, InlinePageletForm
from pagelets import models as pagelets
from pagelets import admin as pagelets_admin
from sample_project.blog.widgets import WYMEditor

class PostAdmin(admin.ModelAdmin):
    form = PostAdminModelForm
    class Media:
        css = {
            "all": (
                    "css/overlay.css",
                   )
        }
        js = ("js/jquery-1.4.2.min.js",
              "js/file-picker.js", "js/jquery.tools.min.js",
              "js/plupload.full.min.js",)
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)
