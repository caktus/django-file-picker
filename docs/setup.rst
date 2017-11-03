.. _setup:

Basic Setup
===========

Here's an example of how to support uploading and linking to files and images
when editing a text field in a model while in the Django admin interface.

#. Use or create a model to contain the text field(s) to be edited
   by the user.  Here we will use the Post model from ``sample_project.article``.
   It has two text fields, Body and Teaser.

#. The files and images are tracked using their own models.
   For simplicity here we will use the models in ``file_picker.uploads``: Image and File.
   (You won't see them mentioned in the code below - more on that shortly.)

#. To use the pickers on both the teaser and body fields, use a *formfield_override*
   in the model's admin class
   to override the widget with the ``file_picker.widgets.SimpleFilePickerWidget``::

    import file_picker
    from django.contrib import admin
    from sample_project.article import models as article_models

    class PostAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {
                'widget': file_picker.widgets.SimpleFilePickerWidget(pickers={
                    'image': "images", # a picker named "images" from file_picker.uploads
                    'file': "files", # a picker named "files" from file_picker.uploads
                }),
            },
        }

        class Media:
            js = ("http://cdn.jquerytools.org/1.2.5/full/jquery.tools.min.js",)

    admin.site.register(article_models.Post, PostAdmin)

There's a lot going on behind the scenes here to make this work. Some of it:

* ``file_picker/uploads/file_pickers.py`` defines two forms,
  defines two picker objects to use those forms, and then registers those two
  pickers to be used with the ``Image`` and ``File`` models mentioned earlier.

* ``file_picker/uploads/file_pickers.py`` needs to be imported for its code to run.
  That happens because 'file_picker.uploads' has been added to ``INSTALLED_APPS``
  during the basic installation of django-file-picker.

Simple File Picker Widget
-------------------------

.. class:: file_picker.widgets.SimpleFilePickerWidget

To use the simple file picker widget, override the desired form field's widget.
It takes a dictionary with expected keys `"image"` and/or `"file"` which
define which link to use, i.e. "Add Image" and/or "Add File".
