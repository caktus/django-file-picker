django-file-picker
==================

django-file-picker is a pluggable Django application used for uploading,
browsing, and inserting various forms of media into HTML form fields.

When a user is editing some content, and they want to insert a link to
a file or image into their content, possibly uploading the image or file
in the process, django-file-picker provides the tools to do that.

Using jQuery Tools, django-file-picker integrates seamlessly into pre-existing pages by
installing an overlay that lists file details and, when applicable, image
thumbnails. New files can also be uploaded from within the overlay (via AJAX
Upload).

django-file-picker provides a few optional extensions to help get started,
including ``file_picker.uploads``, an app with pre-built Image and File models, and
``file_picker.wymeditor``, an app that integrates with
`WYMeditor <http://www.wymeditor.org/>`_, a web-based
WYSIWYM (What You See Is What You Mean) XHTML editor. These extensions are
provided for convenience and can easily be replaced by custom modules.

For more complete documentation, see `<http://django-file-picker.readthedocs.org>`_

Dependencies
------------

Required
````````
* Python 2.7, 3.4, 3.5 and 3.6
* `Django 1.8 to 1.11 (inclusive) <http://www.djangoproject.com/>`_
* sorl-thumbnail==12.4a1
* `jQuery 1.4.x <http://www.jquery.com/>`_
* `jQuery Tools 1.2.x <http://flowplayer.org/tools/>`_
* `AJAX Upload <http://valums.com/ajax-upload/>`_ (included)

Optional
````````
* `django.contrib.staticfiles <https://docs.djangoproject.com/en/1.8/howto/static-files/>`_
* `WYMeditor 0.5 <http://www.wymeditor.org/>`_

  If you are using ``django.contrib.staticfiles``, then add ``file_picker`` to your INSTALLED_APPS
  to include the related css/js.

  Otherwise make sure to include the contents of the static folder in your project's
  media folder.

..  _installation:

Basic Installation
------------------

#. Add ``file_picker`` and ``sorl.thumbnail`` to INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        'file_picker',
        'file_picker.uploads', # file and image Django app
        'file_picker.wymeditor', # optional WYMeditor plugin
        'sorl.thumbnail',  # required
    )

   ``file_picker.uploads`` will automatically create two pickers named 'images' and 'files'.

Note: sorl-thumbnail was out of support for a number of years, but there is now a new pre-release that seems to work, which you can install using::

    $ pip install --pre sorl-thumbnail==12.4a1

Hopefully newer releases will come soon.

#. Add the ``file_picker`` URLs to urls.py, e.g.::

    from django.conf.urls import include, url
    import file_picker

    urlpatterns = [
        # ...
        url(r'^file-picker/', include(file_picker.site.urls)),
        # ...
    ]

Development sponsored by `Caktus Consulting Group, LLC. <https://www.caktusgroup.com/services/>`_.
