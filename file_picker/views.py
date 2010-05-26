from django.utils import simplejson as json
from django.http import HttpResponse


class FilePicker(object):
    model = None

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.list, name='file-list')
        )
        return urlpatterns
    urls = property(get_urls)
    
    def append(self, obj):
        return {'name': unicode(obj), 'url': obj.file.url}

    def list(self, request):
        data = {}
        result = []
        for obj in self.model.objects.all():
            result.append(self.append(obj))
        data['result'] = result
        return HttpResponse(json.dumps(data), mimetype='application/json')
