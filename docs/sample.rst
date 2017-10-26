Running the Sample Project
===============================

django-file-picker includes a sample project to use as an example. You can run the sample project like so::

    ~$ mkvirtualenv --distribute filepicker-sample
    (filepicker-sample)~$ pip install "django>=1.8,<1.11"
    (filepicker-sample)~$ git clone git://github.com/caktus/django-file-picker.git
    (filepicker-sample)~$ cd django-file-picker/
    (filepicker-sample)~/django-file-picker$ python setup.py develop
    (filepicker-sample)~/django-file-picker$ cd sample_project/
    (filepicker-sample)~/django-file-picker/sample_project$ ./manage.py migrate
    (filepicker-sample)~/django-file-picker/sample_project$ ./manage.py createsuperuser
    (filepicker-sample)~/django-file-picker/sample_project$ ./manage.py runserver

Then go to the `admin <http://localhost:8000/admin/>`_, log in, and add an Article Post. There will be 2
links to 'Insert File' and 'Insert Image' which will pop up the File Picker dialog.
