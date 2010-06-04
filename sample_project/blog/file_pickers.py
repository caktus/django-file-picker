from sample_project.blog.models import Image

import file_picker

file_picker.site.register(Image, name='blog')
