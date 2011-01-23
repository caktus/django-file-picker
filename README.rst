django-file-picker
==================

Pluggable Django file picker with AJAX upload support.

Dependencies
------------

Required
````````
* `Django 1.2.x <http://www.djangoproject.com/>`_
* sorl-thumbnail==3.2.5
* `jQuery 1.4.2 <http://www.jquery.com/>`_
* `jQuery Tools 1.2.2 <http://flowplayer.org/tools/>`_
* `AJAX Upload <http://valums.com/ajax-upload/>`_ (included)

Optional
````````
* `WYMeditor 0.5 <http://www.wymeditor.org/>`_

Installation and Setup
----------------------

1) Update INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        # ...
        'file_picker',
        'file_picker.uploads', # optional file and image Django app
        'file_picker.wymeditor', # optional WYMeditor plugin
        # ...
    )

2) Add the file picker URLs to urls.py, e.g.::

    import file_picker
    file_picker.autodiscover()

    urlpatterns = patterns('',
        # ...
        (r'^file-picker/', include(file_picker.site.urls)),
        # ...
    )

3) Register a model with file picker via <app>/file_pickers.py::

    import file_picker
    from myapp.models import Image
    
    file_picker.site.register(Image)

Development sponsored by `Caktus Consulting Group, LLC. <http://www.caktusgroup.com/services>`_.

