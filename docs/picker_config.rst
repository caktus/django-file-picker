Creating Custom Pickers
***********************

File Picker offers many ways to create custom pickers
and assign them to your own models.

The FilePickerBase Class
========================

The base file picker class has a mixture of class based views and helper functions
for building the colorbox on the page.  File pickers should be included in the 
*file_picker.py* file in the root directory of any app so that the auto-discovery
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

* *form*- If left blank is created by building a *ModelForm* from the model defined 
  in the register function.  It is used to build the form on the Upload tab.

* *link_headers*- Defines the headers for the first set of columns which are used 
  to insert content into the textbox or WYSIWYG of your choice.  By default it
  converts _ to ' ' and capitalizes first letter of the fields name.

* *columns*- Defines the fields you want to be included on the listing page
  and their ordering.  
* *extra_headers*- The list is used to define the headers for the columns
  and needs to be in the same order as columns.  
* *ordering*- Defines the order of items on the listing page in 
  to be used as ``query_set.order_by('-date')``.

Methods
-------

The three main methods consist of *append*, *list*, and *upload_file*.  List and upload_file
take in the request object and act as views while append takes in an model item and helps
build the JSON output for list.  Other methods are available but typically do not 
need to be modified.

append(obj)
^^^^^^^^^^^

This method takes in *obj* which is a item from the model and outputs a dictionary
to be used by list.  This dictoinary is of the form.::

    {
        'name': 'Name for the object.', 
        'url': 'The url to the file.',
        'extra': {
            'column_name_1': 'value',
            'column_name_2': 'value',
        },
        'insert': ['string/html to insert if first link is clicked', 'for second link',],
        'link_content': ['string to show on first insert link', 'for second link',],
    }

As a note the *link_content* list and insert list must be the same length, as well as
the extra dictionary and the *link_headers* attribute.

list(request)
^^^^^^^^^^^^^

This takes in a *request* object and outputs.::

    {
        'page': Integer of current,
        'pages': List of pages,
        'search': The current search term,
        'result': List returned from ,
        'has_next': Lets the paginator know whether to hide/show the next button.,
        'has_previous': Same as above for previous button.,
        'link_headers': List of link headers either generated or defined by the attribute.,
        'extra_headers': List of the extra headers made in the same we as above.,
        'columns': List of column names to be included(same as the columns attribute.),
    }

upload_file(request)
^^^^^^^^^^^^^^^^^^^^

Builds the upload file form and is used to upload files in two steps, 
file first then the other form parameters.

If called without a POST it returns a JSON dictionary with the key form
with an html block for the form.

If called with a file and then with the post, its a two step process.  If the form
passed on the second step it returns the result of append for the object which 
was just created.



