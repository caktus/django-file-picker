from sorl.thumbnail.main import DjangoThumbnail 

from sample_project.blog.models import Image

import file_picker


class ImagePicker(file_picker.FilePickerBase):
    
    def get_queryset(self,search):
        return Image.objects.filter(name__icontains=search)
    
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
    
file_picker.site.register(Image, ImagePicker, name='blog')
