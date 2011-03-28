from django.contrib import admin
from file_picker.uploads import models as upload_models

admin.site.register(upload_models.Image)
admin.site.register(upload_models.File)
