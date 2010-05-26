from django.contrib import admin
from sample_project.blog.models import Post, Image
from sample_project.blog.forms import ImageForm


class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/ui-lightness/jquery-ui-1.8.1.custom.css",)
        }
        js = ("js/jquery-1.4.2.min.js", "js/jquery-ui-1.8.1.custom.min.js",
              "js/file-picker.js")
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)
