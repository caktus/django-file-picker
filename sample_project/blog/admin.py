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
            "all": ("css/ui-lightness/jquery-ui-1.8.1.custom.css",)
        }
        js = ("js/jquery-1.4.2.min.js", "js/jquery-ui-1.8.1.custom.min.js",
              "js/file-picker.js", "js/jquery.tools.overlay.js")
admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)


class PageletAdmin(pagelets_admin.PageletAdmin):    
    form = PageletForm
    class Media:
        css = {
            "all": ("css/ui-lightness/jquery-ui-1.8.1.custom.css",)
        }
        js = ("js/jquery-1.4.2.min.js", "js/jquery-ui-1.8.1.custom.min.js",
              "js/file-picker.js")
admin.site.unregister(pagelets.Pagelet)
admin.site.register(pagelets.Pagelet, PageletAdmin)


class InlinePageletAdmin(pagelets_admin.InlinePageletAdmin):
    form = InlinePageletForm


class PageAdmin(pagelets_admin.PageAdmin):    
    inlines = [InlinePageletAdmin, pagelets_admin.SharedPageletAdmin,
           pagelets_admin.InlinePageAttachmentAdmin]
    class Media:
        css = {
            "all": ("css/ui-lightness/jquery-ui-1.8.1.custom.css",)
        }
        js = ("js/jquery-1.4.2.min.js", "js/jquery-ui-1.8.1.custom.min.js",
              "js/file-picker.js")
admin.site.unregister(pagelets.Page)
admin.site.register(pagelets.Page, PageAdmin)
