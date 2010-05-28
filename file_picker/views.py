from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseServerError
from django.core.paginator import Paginator, EmptyPage

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

    def get_queryset(self,search):
        return self.model.objects.all()

    def list(self, request):
        form = QueryForm(request.GET)
        if not form.is_valid():
            return HttpResponseServerError()
        page = form.cleaned_data['page']
        result = []
        qs = self.get_queryset(form.cleaned_data['search'])
        pages = Paginator(qs, self.page_size)
        try:
            page_obj = pages.page(page)
        except EmptyPage:
            return HttpResponseServerError()
        for obj in page_obj.object_list:
            result.append(self.append(obj))
        data = {
            'page': page,
            'result': result,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
