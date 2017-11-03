Detailed Instructions
=====================

The situation where django-file-picker is useful is when you have a user
editing a text field in a form, and you want them to be able to insert
the paths to images and/or files, either ones that have previously been
uploaded, or new ones they upload at the time.

So to start with, you'll have a form with a text field::

    class MyForm(forms.Form):
        my_text = forms.CharField(widget=forms.TextArea)

To insert django-file-picker, we'll tell Django we want to use a different
widget for the ``my_text`` field. This widget will be an instance of
``file_picker.widgets.FilePickerWidget`` or a subclass. For this example,
we'll use ``file_picker.widgets.SimpleFilePickerWidget`` because it has some
buit-in appearance things already set, but later you can customize the appearance
by using your own widget::

    from django import forms
    from file_picker.widgets import SimpleFilePickerWidget

    class MyForm(forms.Form):
        my_text = forms.CharField(
            widget = SimpleFilePickerWidget(...)

File picker widgets have a required argument, ``pickers``, which should be
a dictionary with keys ``"image"``, ``"file"``, or both::

    from django import forms
    from file_picker.widgets import SimpleFilePickerWidget

    class MyForm(forms.Form):
        my_text = forms.CharField(
            widget = SimpleFilePickerWidget(
                pickers = {
                    'image': 'images',
                    'file': 'files',
            )

The values of the items in the pickers dictionary are the names under which pickers
have previously been registered. In this case, we're relying on the knowledge
that we've added ``file_picker.uploads`` to our ``INSTALLED_APPS``, and
the uploads app's file_picker.py file registered two pickers. That code looks like this::

    import file_picker

    file_picker.site.register(Image, ImagePicker, name='images')
    file_picker.site.register(File, FilePicker, name='files')

That raises the question, what is a picker?  A picker is a previously
registered name that has linked to it a model and a subclass of
``file_picker.ImagePickerBase`` or ``file_picker.FilePickerBase``.
In the code above, ``Image`` and ``File`` are models, and the two
``XxxxPicker`` identifiers name such classes.

Let's look first at the models::

    class File(BaseFileModel):
        """ Basic file field model """
        file = models.FileField(upload_to='uploads/files/')


    class Image(BaseFileModel):
        """ Basic image field model """
        file = models.ImageField(upload_to='uploads/images/')

We can see that each one has a ``file`` column with a Django FileField
or ImageField.  They both inherit from abstract model ``BaseFileModel``,
which adds a bunch of handy fields like ``name``, ``description``,
``file_type``, etc.

The purpose of the models is to track the uploaded files, and this looks
reasonable for that.  But how does django-file-picker use these models? Or
in other words, how much of this code is required by django-file-picker and
how much can we do what we like with?

For that, we need to look at the picker classes.  Here's what the ``FilePicker``
class looks like::

    class FilePicker(file_picker.FilePickerBase):
        form = FileForm
        columns = ('name', 'file_type', 'date_modified')
        extra_headers = ('Name', 'File type', 'Date modified')

The ``columns`` are field names from the file tracking model, and the
``extra_headers`` the corresponding headers for those fields. So it seems reasonable
to guess that the picker widget is going to display those columns when it is listing
the uploaded files, and we can see that that part is completely customizable.

There's more about pickers in the docs elsewhere - look for the part
about writing custom pickers.

What about the form?  You can leave the ``form`` off of your picker class and
file-picker will generate a form on the fly, but in this case, the code provides
its own form.  Here's ``FileForm``::

    class FileForm(forms.ModelForm):
        file = forms.CharField(widget=forms.widgets.HiddenInput())

        class Meta(object):
            model = File
            fields = ('name', 'description')

        def save(self, commit=True):
            image = super(FileForm, self).save(commit=False)
            # Strip any directory names from the filename
            file_path = os.path.basename(self.cleaned_data['file'])
            fh = ContentFile(open(self.cleaned_data['file'], 'rb').read())
            image.file.save(file_path, fh)
            if commit:
                image.save()
            return image

This is more complicated. This is the form that will be used when the user wants
to upload a new file. From ``Meta.fields``, we can see that the user will only
have to enter the name and description. But there's also a hidden ``file`` field,
of type CharField. It looks like this is going to end up with a path to a
temporary file, and when the form is saved, it'll copy that into the file field of
the new model instance and save it.

The ``ImageForm`` is practically identical apart from the model it's associated
with. I don't know why all the common code isn't factored out into a base form
class provided by file_picker.

Again, you don't have to write your own form class if you don't
want to. You can leave out the form attribute
when creating your picker class, and it'll generate the necessary form on the fly.

Your template must load jquery, jquery-ui, and jquery.tools, as well as any media associated with your form by file-picker. Your head section might look like:

.. code-block:: html

    <head>
      <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
      <script src="http://cdn.jquerytools.org/1.2.5/full/jquery.tools.min.js"></script>
      {{ form.media }}
    </head>

Then you can use your form in your template in the usual way. You can start with:

.. code-block:: html

    <form action="." method="POST" >
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">Submit</button>
    </form>

For more information, I recommend reading the code of django-file-picker,
especially the ``uploads`` app,
``forms.py`` which has the base class used to generate new forms for pickers,
and the ``views.py`` file which handles the uploads.
