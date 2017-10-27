Creating Custom Pickers
***********************

File Picker offers many ways to create custom pickers
and assign them to your own models.

The FilePickerBase Class
========================

The base file picker class has a mixture of class based views and helper functions
for building the colorbox on the page.  File pickers should be included in the
*file_pickers.py* file in the root directory of any app so that the auto-discovery
process can find it.


Attributes
----------

Each picker can take a set of attributes for easy customization.::

    from myapp.models import CustomModel
    from myapp.forms import CustomForm
    import file_pickers

    class CustomPicker(file_picker.FilePickerBase):
        form = CustomForm
        page_size = 4
        link_headers = ['Insert File',]
        columns = ['name', 'body', 'description',]
        extra_headers = ['Name', 'Body', 'Description',]
        ordering = '-date'

    file_picker.site.register(CustomModel, CustomPicker, name='custom')

None of these attributes are required and they all have sane defaults.

* *form*- If not set, a *ModelForm* is created using the model defined
  in the register function.  This is used to build the form on the Upload tab.

* *link_headers*- Defines the headers for the first set of columns which are used
  to insert content into the textbox or WYSIWYG widget of your choice.  By default, it
  converts _ to ' ' and capitalizes the first letter of the field's name.

* *columns*- Defines the fields you want to be included on the listing page
  and their ordering.
* *extra_headers*- This list is used to display the headers for the columns
  and needs to be in the same order as *columns*.
* *ordering*- Defines the order of items on the listing page. In this example,
  the code would run ``query_set.order_by('-date')``. If no ordering is
  provided, we'll order by ``-pk``.


Methods
-------

The three main methods consist of *append*, *list*, and *upload_file*. *List*
and *upload_file* take a request object and act as views, while *append* takes
a model instance and builds the JSON output for list. Other methods are
available but typically do not need to be modified.

append(obj)
^^^^^^^^^^^

This method takes *obj* which is a model instance and returns a dictionary
to be used by *list*.  This dictionary is of the form::

    {
        'name': 'Name for the object.',
        'url': 'The url to the file.',
        'extra': {
            'column_name_1': 'value',
            'column_name_2': 'value',
        },
        'insert': [
            'text or html to insert if first link is clicked',
            'text or html to insert if second link is clicked',
        ],
        'link_content': [
            'string to show on first insert link',
            'string to show on second insert link',
        ],
    }

The *link_content* list, *insert* list, and *extra* dictionary must all be the
same length, and must match the length of the *link_headers* of your custom FilePicker.

list(request)
^^^^^^^^^^^^^

This takes a *request* object and returns::

    {
        'page': 1-based integer representing current page number,
        'pages': List of pages,
        'search': The current search term,
        'result': List returned from *append*,
        'has_next': Boolean telling paginator whether to show the next button,
        'has_previous': Boolean telling paginator whether to show the previous button.,
        'link_headers': List of link headers defined by the Picker attribute (or generated if not defined),
        'extra_headers': List of the extra_headers specified by the Picker attribute,
        'columns': List of column names specified by the Picker attribute,
    }

upload_file(request)
^^^^^^^^^^^^^^^^^^^^

This takes a *request* object and builds the upload file form, which is used
to upload files in two steps: first the file, and then the other form parameters.

If called without POST data it returns a JSON dictionary with the key ``form``
containing the HTML representation of the form.

If called with a file and then with the POST data, it performs a two step
process. If the form validates successfully on the second step it returns the
result of *append* for the object which was just created.
