.. _uploads:


The Uploads App
=======================

The uploads app is designed to make it easy to get File Picker up and running without
having to add models or register them with ``file_picker``. The uploads app includes two
simple pickers which can be attached to your own project's text fields. For installation
instructions, check out :ref:`setup`

FilePicker
----------

.. class:: file_picker.uploads.file_pickers.FilePicker

Is a simple class based off of the ``file_picker.FilePickerBase``
which is connected to the *File* model and can be found in the Uploads admin
section.

ImagePicker
-----------

.. class:: file_picker.uploads.file_pickers.ImagePicker

Is a simple class based off of the ``file_picker.ImagePickerBase``
which is connected to the *Image* model and can be found in the Uploads admin
section.

Simple File Picker Widget
-------------------------

These pickers can be used like any other.  Below is an example of how to add them
on a single text field::

    body = forms.TextField(
                widget=file_picker.widgets.SimpleFilePickerWidget(pickers={
                    'file': "files",
                    'image': "images",
                }))

Where the `"file"` and `"image"` keywords add classes to the inputs, so that the links
for the overlay can be added.  They can also be added to all fields in a form by
using the *formfield_overrides* as in:ref:`setup`.
