from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^blog/', include('sample_project.blog.urls')),
    (r'^article/', include('sample_project.article.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if getattr(settings, 'SERVE_STATIC_MEDIA', False):
    urlpatterns += patterns('', (
            r'^%s(?P<path>.*)' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        )
    )
    
urlpatterns += patterns('',
    (r'^%spagelets/', include('pagelets.urls.management')),
    (r'^%s', include('pagelets.urls.content')),
)
