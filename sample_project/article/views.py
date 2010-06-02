import os
import sys
import tempfile

from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from sample_project.article.models import Image
from sample_project.article.forms import AjaxImageForm

from file_picker.views import FilePicker

from sorl.thumbnail.main import DjangoThumbnail 


class ImagePicker(FilePicker):
    model = Image
    
    def get_queryset(self,search):
        return Image.objects.filter(name__icontains=search)
    
    @csrf_exempt
    def upload_file(self, request):
        if request.GET and 'name' in request.GET:
            fn = add_unique_postfix('/tmp/%s' % request.GET['name'])
            tempfile.NamedTemporaryFile([mode='w+b'[, bufsize=-1[, suffix=''[, prefix='tmp'[, dir=None[, delete=True]]]]]])
            f = open(fn, 'wb+')
            f.write(request.raw_post_data)
            f.close()
            return HttpResponse(fn, mimetype='application/json')
        else: 
            if request.POST:
                form = AjaxImageForm(request.POST)
                if form.is_valid():
                    item = self.model(
                        name=form.cleaned_data['name']
                    )
                    item.file.save(request.POST['file'],ContentFile(open(request.POST['file'],'r').read()))
                    item.save()
            else:
                form = AjaxImageForm()
            form_str = render_to_string('article/upload_form.html', {'form': form})
            data = { 'form': form_str }
            return HttpResponse(json.dumps(data), mimetype='application/json') 
    
    def append(self, obj):
        thumb = DjangoThumbnail(obj.file, (150, 150))
        return {
            'name': unicode(obj), 'url': obj.file.url,
            'thumb': {
                'url': thumb.absolute_url,
                'width': thumb.width(),
                'height': thumb.height(),
            },
            'insert': '<img src="%s" />' % obj.file.url
        }
    
file_picker = ImagePicker()


def add_unique_postfix(fn):
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s(%d)%s' % (name, i, ext))

    for i in xrange(2, sys.maxint):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

