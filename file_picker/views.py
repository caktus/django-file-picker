import datetime
import json
import logging
import os
import tempfile
import traceback

from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
from django.utils.text import capfirst

from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail import get_thumbnail

from file_picker.forms import QueryForm, model_to_AjaxItemForm


logger = logging.getLogger(__name__)


class FilePickerBase(object):
    model = None
    form = None
    page_size = 4
    link_headers = ['Insert File', ]
    extra_headers = None
    columns = None
    ordering = None

    def __init__(self, name, model):
        self.name = name
        self.model = model
        if not self.form:
            self.form = model_to_AjaxItemForm(self.model)
        self.field_names = [f.name for f in model._meta.get_fields()]
        build_headers = not self.columns or not self.extra_headers
        if not self.columns:
            self.columns = self.field_names
        extra_headers = []
        for field_name in self.field_names:
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
        for field_name in self.columns:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                self.field_names.remove(field_name)
                continue
            extra_headers.append(capfirst(field.verbose_name))
        if build_headers:
            self.extra_headers = extra_headers

    def protect(self, view, csrf_exempt=False):
        def wrapper(*args, **kwargs):
            data = {}
            try:
                return view(*args, **kwargs)
            except Exception as e:
                logger.exception("error in view")
                data['errors'] = [traceback.format_exc(e)]
            return HttpResponse(json.dumps(data), content_type='application/json')
        wrapper.csrf_exempt = csrf_exempt
        return wrapper

    def get_urls(self):
        urlpatterns = [
            url(r'^$', self.setup, name='init'),
            url(r'^files/$', self.list, name='list-files'),
            url(r'^upload/file/$', self.protect(self.upload_file, True),
                name='upload-file'),
        ]
        return (urlpatterns, None, self.name)
    urls = property(get_urls)

    def setup(self, request):
        data = {}
        data['urls'] = {
            'browse': {'files': reverse('filepicker:%s:list-files' % self.name)},
            'upload': {'file': reverse('filepicker:%s:upload-file' % self.name)},
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

    def append(self, obj):
        extra = {}
        for name in self.columns:
            value = getattr(obj, name)
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = value.strftime('%b %d, %Y')
            else:
                value = str(value)
            extra[name] = value
        return {
            'name': str(obj),
            'url': getattr(obj, self.field).url,
            'extra': extra,
            'insert': [getattr(obj, self.field).url, ],
            'link_content': ['Click to insert'],
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
        else:
            # Need to default to some kind of ordering since we paginate
            queryset = queryset.order_by('-pk')
        return queryset

    def upload_file(self, request):
        if 'userfile' in request.FILES:
            name, ext = os.path.splitext(request.FILES['userfile'].name)
            fn = tempfile.NamedTemporaryFile(prefix=name, suffix=ext, delete=False)
            f = request.FILES['userfile']
            for chunk in f.chunks():
                fn.write(chunk)
            fn.close()
            return HttpResponse(json.dumps({'name': fn.name}), content_type='application/json')
        else:
            form = self.form(request.POST or None)
            if form.is_valid():
                obj = form.save()
                data = self.append(obj)
                return HttpResponse(json.dumps(data),
                                    content_type='application/json')
            data = {'form': form.as_table()}
            return HttpResponse(json.dumps(data), content_type='application/json')

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
            'pages': list(pages.page_range),
            'search': form.cleaned_data['search'],
            'result': result,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'link_headers': self.link_headers,
            'extra_headers': self.extra_headers,
            'columns': self.columns,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')


class ImagePickerBase(FilePickerBase):
    link_headers = ['Thumbnail', ]

    def append(self, obj):
        json = super(ImagePickerBase, self).append(obj)
        img = '<img src="{0}" alt="{1}" width="{2}" height="{3}" />'
        try:
            thumb = get_thumbnail(obj.file.path, '150x150', crop='center', quality=99)
        except ThumbnailError:
            logger.exception()
            thumb = None
        if thumb:
            json['link_content'] = [img.format(thumb.url, 'image', thumb.width, thumb.height), ]
            json['insert'] = ['<img src="%s" />' % getattr(obj, self.field).url, ]
        else:
            json['link_content'] = [img.format('', 'Not Found', 150, 150), ]
            json['insert'] = [img.format('', 'Not Found', 150, 150), ]
        return json
