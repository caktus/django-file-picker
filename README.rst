django-file-picker
==================

django-file-picker is a pluggable Django application used for uploading,
browsing, and inserting various forms of media into HTML form fields.

Using jQuery Tools, file_picker integrates seamlessly into pre-existing pages by
installing an overlay that lists file details and, when applicable, image
thumbnails. New files can also be uploaded from within the overlay (via AJAX
Upload).

``file_picker`` provides a few optional extensions to help get started,
including ``file_picker.uploads``, an app with pre-built Image and File models, and
``file_picker.wymeditor``, an app that integrates with
`WYMeditor <http://www.wymeditor.org/>`_, a web-based
WYSIWYM (What You See Is What You Mean) XHTML editor. These extensions are
provided for convenience and can easily be replaced by custom modules.


Dependencies
------------

Required
````````
* `Django 1.2 or higher. <http://www.djangoproject.com/>`_
* sorl-thumbnail==3.2.5
* `jQuery 1.4.x <http://www.jquery.com/>`_
* `jQuery Tools 1.2.x <http://flowplayer.org/tools/>`_
* `AJAX Upload <http://valums.com/ajax-upload/>`_ (included)

Optional
````````
* `django-staticfiles <https://github.com/jezdez/django-staticfiles>`_
* `WYMeditor 0.5 <http://www.wymeditor.org/>`_

  If you are using *django-staticfiles* (or ``django.contrib.staticfiles`` in Django
  1.3) then add ``file_picker`` to your INSTALLED_APPS to include the related css/js.

  Otherwise make sure to include the contents of the static folder in your projects
  media folder.

..  _installation:

Basic Installation
------------------

#. Add ``file_picker`` to INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        'file_picker',
        'file_picker.uploads', # file and image Django app
        'file_picker.wymeditor', # optional WYMeditor plugin
    )

   ``file_picker.uploads`` will automatically create two pickers name 'images' and 'files'.

#. Add the ``file_picker`` URLs to urls.py, e.g.::

    import file_picker
    file_picker.autodiscover()

    urlpatterns = patterns('',
        # ...
        (r'^file-picker/', include(file_picker.site.urls)),
        # ...
    )

Development sponsored by `Caktus Consulting Group, LLC. <http://www.caktusgroup.com/services>`_.

