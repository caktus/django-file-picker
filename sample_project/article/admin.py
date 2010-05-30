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
              #"js/gears_init.js",
              #"http://bp.yahooapis.com/2.4.21/browserplus-min.js",
              "js/plupload.full.min.js",
              #"js/plupload.gears.js",
              #"js/plupload.silverlight.js",
              #"js/plupload.flash.js",
              #"js/plupload.browserplus.js",
              #"js/plupload.html5.js",
              #"js/jquery.plupload.queue.js",
        )
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)
