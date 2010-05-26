from django.contrib import admin
from sample_project.blog.models import Post, Image


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)
