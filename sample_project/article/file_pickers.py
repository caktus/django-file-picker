from sample_project.article.models import Image

import file_picker

file_picker.site.register(Image, name='article')
