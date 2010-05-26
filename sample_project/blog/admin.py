from django.contrib import admin
from sample_project.blog.models import Post


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)
