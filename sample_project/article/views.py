from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson as json

from sample_project.article.models import Image
from sample_project.article.forms import AjaxImageForm

from file_picker.views import FilePicker

from sorl.thumbnail.main import DjangoThumbnail 


class ImagePicker(FilePicker):
    model = Image
    
    def get_queryset(self,search):
        return Image.objects.filter(name__icontains=search)
    
    def upload_file(self, request):
        if request.POST:
            form = AjaxImageForm(request.POST)
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
