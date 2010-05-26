from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseServerError

from file_picker.forms import QueryForm


class FilePicker(object):
    model = None
    page_size = 4

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
        form = QueryForm(request.GET)
        if not form.is_valid():
            return HttpResponseServerError()
        page = form.cleaned_data['page']
        start = page * self.page_size
        end = start + self.page_size
        result = []
        for obj in self.model.objects.all()[start:end]:
            result.append(self.append(obj))
        data = {
            'page': page,
            'result': result,
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
