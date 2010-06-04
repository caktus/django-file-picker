import os
import tempfile

from django.db import models
from django.utils import simplejson as json
from django.utils.text import capfirst
from django.http import HttpResponse, HttpResponseServerError
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt

from sorl.thumbnail.main import DjangoThumbnail

from file_picker.forms import QueryForm, model_to_AjaxItemForm


class FilePickerBase(object):
    model = None
    form = None
    page_size = 4

    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.form = model_to_AjaxItemForm(self.model)
        self.field_names = model._meta.get_all_field_names()
        self.field_labels = {}
        for field_name in model._meta.get_all_field_names():
            field = model._meta.get_field(field_name)
            if type(field) == models.ImageField:
                self.image_field = field_name
                self.field_names.remove(field_name)
            elif type(field) in (models.FileField, models.ForeignKey, models.ManyToManyField):
                self.field_names.remove(field_name)
            else:
                self.field_labels[field_name] = capfirst(field.verbose_name)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.setup, name='init'),
            url(r'^files/$', self.list, name='list-files'),
            url(r'^upload/file/$', self.upload_file, name='upload-file'),
        )
        return (urlpatterns, None, self.name)
    urls = property(get_urls)
    
    def setup(self, request):
        data = {}
        data['urls'] = {
            'browse': {'files': reverse('filepicker:%s:list-files' % self.name)},
            'upload': {'file': reverse('filepicker:%s:upload-file' % self.name)},
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    
    def append(self, obj):
        return {'name': unicode(obj), 'url': obj.file.url}

    def get_queryset(self,search):
        return self.model.objects.all()

    @csrf_exempt
    def upload_file(self, request):
        if request.GET and 'name' in request.GET:
            name, ext = os.path.splitext(request.GET['name'])
            fn = tempfile.NamedTemporaryFile(prefix=name, suffix=ext, delete=False)
            fn.write(request.raw_post_data)
            fn.close()
            return HttpResponse(fn.name, mimetype='application/json')
        else: 
            if request.POST:
                form = self.form(request.POST)
                if form.is_valid():
                    obj = form.save()
                    data = self.append(obj)
                    return HttpResponse(
                        json.dumps(data), mimetype='application/json'
                    )
            else:
                form = self.form()
            form_str = form.as_table()
            data = { 'form': form_str }
            return HttpResponse(json.dumps(data), mimetype='application/json') 

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
            'pages': pages.page_range,
            'search': form.cleaned_data['search'],
            'result': result,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')


class ImagePickerBase(FilePickerBase):
    def append(self, obj):
        thumb = DjangoThumbnail(getattr(obj, self.image_field), (150, 150))
        extra = {}
        for name in self.field_names:
            extra[self.field_labels[name]] = str(getattr(obj, name))
        return {
            'url': getattr(obj, self.image_field).url,
            'thumb': {
                'url': thumb.absolute_url,
                'width': thumb.width(),
                'height': thumb.height(),
            },
            'insert': '<img src="%s" />' % getattr(obj, self.image_field).url,
            'extra': extra
        }
