from sample_project.blog.models import Image

from file_picker.views import FilePicker

from sorl.thumbnail.main import DjangoThumbnail 

class ImagePicker(FilePicker):
    model = Image
    
    def append(self, obj):
        thumb = DjangoThumbnail(obj.file, (20,20))
        return {
            'name': unicode(obj), 'url': obj.file.url,
            'thumb_url': thumb.absolute_url,
        }
    
file_picker = ImagePicker()
