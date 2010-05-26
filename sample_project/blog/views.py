from sample_project.blog.models import Image

from file_picker.views import FilePicker


class ImagePicker(FilePicker):
    model = Image

file_picker = ImagePicker()
