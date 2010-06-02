import os
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
            name, ext = os.path.splitext(request.GET['name'])
            fn = tempfile.NamedTemporaryFile(prefix=name, suffix=ext, delete=False)
            fn.write(request.raw_post_data)
            fn.close()
            fn.name
            return HttpResponse(fn.name, mimetype='application/json')
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
