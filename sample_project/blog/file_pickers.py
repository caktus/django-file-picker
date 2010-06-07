from sample_project.blog.models import Image, File

import file_picker

file_picker.site.register(Image, name='blog-image')
file_picker.site.register(File, name='blog-file')
