django-file-picker
==================

Pluggable Django file picker with AJAX upload support.

Dependencies
------------

Required
````````
* `Django 1.2.x <http://www.djangoproject.com/>`_
* sorl-thumbnail==3.2.5
* `jQuery 1.4.x <http://www.jquery.com/>`_
* `jQuery Tools 1.2.x <http://flowplayer.org/tools/>`_
* `AJAX Upload <http://valums.com/ajax-upload/>`_ (included)

Optional
````````
* `WYMeditor 0.5 <http://www.wymeditor.org/>`_

Basic Installation and Setup
----------------------------

1) Add file picker to INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        # ...
        'file_picker',
        'file_picker.uploads', # file and image Django app
        'file_picker.wymeditor', # optional WYMeditor plugin
        # ...
    )

`file_picker.uploads` will automatically create two pickers name 'images' and 'files'.

2) Add the file picker URLs to urls.py, e.g.::

    import file_picker
    file_picker.autodiscover()

    urlpatterns = patterns('',
        # ...
        (r'^file-picker/', include(file_picker.site.urls)),
        # ...
    )

3) Setup widgets and media::

    class PostAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {
                'widget': file_picker.widgets.FilePickerWidget(pickers={
                    'image': "images", # a picker named "images" from file_picker.uploads
                    'file': "files", # a picker named "files" from file_picker.uploads
                }),
            },
        }
    
        class Media:
            css = {"all": ("css/filepicker.overlay.css",)}
            js = ("http://cdn.jquerytools.org/1.2.5/full/jquery.tools.min.js",
                  "js/ajaxupload.js",
                  "js/jquery.filepicker.js",
                  "js/jquery.filepicker.simple.js",)

Development sponsored by `Caktus Consulting Group, LLC. <http://www.caktusgroup.com/services>`_.

