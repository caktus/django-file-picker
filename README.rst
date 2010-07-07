-*- restructuredtext -*-

django-file-picker
==================
Pluggable file picker, which can register any number of models, and be used to
insert images/files from any of those model into any text or wysiwyg
editors.

Install Instructions
____________________
    Assuming django 1.2/1.1, pip, and python are already installed.  This should lead you through the steps required to have a basic file-picker for a textarea.  The file-picker application with inspect the model and build a form and list display for uploads and downloads.  To further customize the picker you can manually set file-picker class to use.

    1. pip install -e hg+http://bitbucket.org/copelco/django-file-picker/#egg=file-picker
    2. Add file-picker to your main url file, similar to admin autodiscover.
        ::

            import file_picker
            file_picker.autodiscover()

    3. Add file-picker to your urlpatterns: (r'^file-picker/', include(file_picker.site.urls))
    4. Create a file called file_pickers and add this to it:
        ::

            import file_picker
            file_picker.site.register(Model, name='url-name')    

        Where Model is the model which you want to pick from and name is the name that will be used for the url entries name.  Multiple models can be registered in this way.
    5. Add the required javascript and css files to the projects media directory.  Overlay.css and file-picker.js can be found in the media directory of the sample project.
        - css/overlay.css
        - js/jquery-1.4.2.min.js
        - js/jquery.tools.min.js
        - js/ajaxupload.js
        - js/file-picker.js

    6. In the form where you plan on using the file-picker use this widget for the textarea you would like to have the file-picker insert the file/image into.  If your using a wysiwyg look at the sample_project.blog.widgets to see how this was done with wymeditor.
        ::
        
            file_picker.widgets.BasicFilePickerWidget(picker="url-name")
                  
                              
Using Custom Pickers
____________________
    For the case where the form or display list comes out incorrectly you can define the class to use like so:
        ::
        
            file_picker.site.register(Model, name='url-name', class_=NewPicker)    

    Where NewPicker extends from filer_picker.views.FilePickerBase or ImagePickerBase like this example which uses a custom form and uses a inserts a "item" in the textarea, this time an image from the "field_to_pick" at 50% its normal size:
        ::
        
            class NewPicker(FilePickerBase):
                form = CustomForm
                def append(self, obj):
                    json = super(NewPicker, self).append(obj)
                    json['insert'] = '<img width="50%" height="50%" src="%s" />' % obj.field_to_pick.url
                    return json
        

Examples
________
A couple of different examples.

ModelAdmin
----------

::
    
    class PostAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {
                'widget': file_picker.widgets.BasicFilePickerWidget(picker="article")
            },
        }

        class Media:
            css = {"all": ("css/overlay.css",)}
            js = ("js/jquery-1.4.2.min.js",
                  "js/jquery.tools.min.js",
                  "js/ajaxupload.js",
                  "js/file-picker.js",)
    admin.site.register(Post, PostAdmin)

Wymeditor
---------
Uses Wymeditor as a wysiwyg and includes buttons for images or files.  Look at the media folder for images to use as icons.
::

    class WymeditorAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {
                'widget': file_picker.widgets.WYMeditorWidget(pickers={
                    'file': 'files',
                    'image': 'images',
                })
            },
        }

        class Media:
            css = {"all": ("css/overlay.css", )}
            js = ("js/jquery-1.4.2.min.js",
                  "wymeditor/jquery.wymeditor.pack.js",
                  "js/jquery.tools.min.js",
                  "js/ajaxupload.js",
                  "js/file-picker.js",
                  "js/file-picker-wymeditor.js",)

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
