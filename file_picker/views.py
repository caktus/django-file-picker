import os
import logging
import traceback
import tempfile

from django.db import models
from django.db.models import Q
from django.utils import simplejson as json
from django.utils.text import capfirst
from django.http import HttpResponse, HttpResponseServerError
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt

from sorl.thumbnail.main import DjangoThumbnail
from sorl.thumbnail.base import ThumbnailException

from file_picker.forms import QueryForm, model_to_AjaxItemForm


class FilePickerBase(object):
    model = None
    form = None
    page_size = 4
    link_header = 'Insert File'
    columns = None
    ordering = None

    def __init__(self, name, model):
        self.name = name
        self.model = model
        if not self.form:
            self.form = model_to_AjaxItemForm(self.model)
        self.field_names = model._meta.get_all_field_names()
        self.field_labels = {}
        for field_name in model._meta.get_all_field_names():
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                self.field_names.remove(field_name)
                continue
            if isinstance(field, (models.ImageField, models.FileField)):
                self.field = field_name
                self.field_names.remove(field_name)
            elif isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                self.field_names.remove(field_name)
            else:
                self.field_labels[field_name] = capfirst(field.verbose_name)

    def protect(self, view, csrf_exempt=False):
        def wrapper(*args, **kwargs):
            data = {}
            try:
                return view(*args, **kwargs)
            except Exception, e:
                logging.exception(e)
                data['errors'] = [traceback.format_exc(e)]
            return HttpResponse(json.dumps(data), mimetype='application/json')
        wrapper.csrf_exempt = csrf_exempt
        return wrapper

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.setup, name='init'),
            url(r'^files/$', self.list, name='list-files'),
            url(r'^upload/file/$', self.protect(self.upload_file, True),
                name='upload-file'),
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
        extra = {}
        if self.columns:
            columns = self.columns
        else:
            columns = self.field_names
        for name in columns:
            extra[self.field_labels[name]] = str(getattr(obj, name))
        return {'name': unicode(obj), 'url': getattr(obj, self.field).url,
            'extra': extra,
            'insert': getattr(obj, self.field).url,
            'link_content': 'Click to insert',
        }

    def get_queryset(self, search):
        qs = Q()
        if search:
            for name in self.field_names:
                comparision = {}
                comparision[name] = search
                qs = qs | Q(name__contains=search)
            queryset = self.model.objects.filter(qs)
        else:
            queryset = self.model.objects.all()
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset

    def upload_file(self, request):
        if 'userfile' in request.FILES:
            name, ext = os.path.splitext(request.FILES['userfile'].name)
            fn = tempfile.NamedTemporaryFile(prefix=name, suffix=ext, delete=False)
            f = request.FILES['userfile']
            for chunk in f.chunks():
                fn.write(chunk)
            fn.close()
            return HttpResponse(json.dumps({ 'name': fn.name }), mimetype='text/html')
        else:
            form = self.form(request.POST or None)
            if form.is_valid():
                obj = form.save()
                data = self.append(obj)
                return HttpResponse(
                    json.dumps(data), mimetype='application/json'
                )
            data = {'form': form.as_table()}
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
            'link_header': self.link_header,
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')


class ImagePickerBase(FilePickerBase):
    link_header = 'Thumbnail'

    def append(self, obj):
        json = super(ImagePickerBase, self).append(obj)
        img = '<img src="{0}" alt="{1}" width="{2}" height="{3}" />'
        try:
            thumb = DjangoThumbnail(getattr(obj, self.field), (150, 150))
        except ThumbnailException:
            thumb = None
        if thumb:
            json['link_content'] = img.format(thumb.absolute_url, 
                                    thumb.width(), thumb.height(),)
            json['insert'] = '<img src="%s" />' % getattr(obj, self.field).url
        else:
            json['link_content'] = img.format('', 'Not Found', 150, 150)
            json['insert'] = img.format('', 'Not Found', 150, 150)
        return json
