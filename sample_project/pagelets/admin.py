from django.contrib import admin

from pagelets import models as pagelets
from pagelets import admin as pagelets_admin


class PageletAdmin(pagelets_admin.PageletAdmin):

    class Media:
        css = {"all": ("css/overlay.css",)}
        js = ("js/jquery-1.4.2.min.js",
              "wymeditor/jquery.wymeditor.pack.js",
              "js/jquery.tools.min.js",
              "js/ajaxupload.js",
              "js/file-picker.js",
              "js/pagelets.js",)

admin.site.unregister(pagelets.Pagelet)
admin.site.register(pagelets.Pagelet, PageletAdmin)


class PageAdmin(pagelets_admin.PageAdmin):    

    class Media:
        css = {"all": ("css/overlay.css",)}
        js = ("js/jquery-1.4.2.min.js",
              "wymeditor/jquery.wymeditor.pack.js",
              "js/jquery.tools.min.js",
              "js/ajaxupload.js",
              "js/file-picker.js",
              "js/pagelets.js",)

admin.site.unregister(pagelets.Page)
admin.site.register(pagelets.Page, PageAdmin)
