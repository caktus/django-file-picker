from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

import file_picker

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^file-picker/', file_picker.site.urls),

    url(r'^%s(?P<path>.*)' % settings.MEDIA_URL.lstrip('/'),
        serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
]
