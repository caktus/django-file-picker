.. _setup:

Basic Setup
===========

#. Use or create a model for storing images and/or files.  For simplicity here
   we will use the models in ``file_picker.uploads``: Image and File.

#. Use or create another model to contain the text field(s) to be inserted
   by the picker.  Here we will use the Post model from ``sample_project.article``.
   It has two text fields, Body and Teaser.

#. To use the pickers on both the teaser and body fields use a *formfield_override*
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


Simple File Picker Widget
-------------------------

.. class:: file_picker.widgets.SimpleFilePickerWidget

To use the simple file picker widget, override the desired form field's widget.
It takes a dictionary with expected keys `"image"` and/or `"file"` which
define which link to use, i.e. "Add Image" and/or "Add File".
