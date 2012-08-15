import os
import file_picker
import datetime

from django.db import models
from django.test import TestCase
from django.core.files import File
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils.text import capfirst


class Image(models.Model):
    """
    Image Model for tests.
    """
    name = models.CharField(max_length=255)
    description_1 = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    file = models.ImageField(upload_to='images/')    


class MockRequest(object):
    """
    Incomplete Mock Request object.
    """
    GET = {}
    POST = {}
    FILES = {}
        

class MockImagePicker(file_picker.ImagePickerBase):
    def __init__(self, name, model, columns, extra_headers, extra={}):
        if columns:
            self.columns = columns
        if extra_headers:
            self.extra_headers = extra_headers
        for key, value in extra.items():
            setattr(self, key, value)
        super(MockImagePicker, self).__init__(name, model)


class BasePickerTest(TestCase):
    """
    Base class to build the 
    """
    def setUp(self):
        self.path = os.path.abspath('%s' % os.path.dirname(__file__))
        self.image_file = File(open(os.path.join(self.path, 'static/img/attach.png')), "test_file.png")
        self.image = Image(
             name = 'Test Image',
             description_1 = 'test desc 1',
             description_2 = 'test desc 2',
             file = self.image_file,
            )
        self.image.save()
        self.request = MockRequest()
    

class TestListPage(BasePickerTest):
    """
    Test listing page.
    """
    def setUp(self):
        super(TestListPage, self).setUp()
        self.field_names = Image._meta.get_all_field_names()
        self.field_names.remove('file')
        
    def test_all_fields(self):
        """
        Test neither columns nor extra_headers defined.
        """
        image_picker = MockImagePicker('image_test', Image, None, None)
        response = image_picker.list(self.request)
        list_resp = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.field_names, list_resp['columns'])
        self.assertEquals([capfirst(Image._meta.get_field(i).verbose_name) \
                for i in self.field_names], list_resp['extra_headers'])

    def test_columns(self):
        """
        Test only columns defined.
        """
        columns = ['description_2', 'name',]
        image_picker = MockImagePicker('image_test', Image, columns, None)
        response = image_picker.list(self.request)
        list_resp = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(columns, list_resp['columns'])
        extra_headers = [capfirst(Image._meta.get_field(i).verbose_name) \
                for i in columns]
        self.assertEquals(extra_headers, list_resp['extra_headers'])
        
    def test_extra_headers(self):
        """
        Test only extra headers defined.  Should ignore it completely.
        """
        image_picker = MockImagePicker('image_test', Image, None, ['Header'])
        response = image_picker.list(self.request)
        list_resp = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.field_names, list_resp['columns'])
        self.assertEquals([capfirst(Image._meta.get_field(i).verbose_name) \
                for i in self.field_names], list_resp['extra_headers'])
                
    def test_columns_and_headers(self):
        """
        Test custom columns and extra headers.
        """
        columns = ['description_2', 'name', 'description_1']
        extra_headers = ['Top Description', 'Image Name', 'Bottom Description']
        image_picker = MockImagePicker('image_test', Image, columns, extra_headers)
        response = image_picker.list(self.request)
        list_resp = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(columns, list_resp['columns'])
        self.assertEquals(extra_headers, list_resp['extra_headers'])
        
    def test_file_list(self):
        """
        Make sure that the file list gives the correct url.
        """
        image_picker = MockImagePicker('image_test', Image, None, None)
        response = image_picker.list(self.request)
        list_resp = json.loads(response.content)
        results = list_resp['result']
        self.assertEquals(len(results), 1)
        result = results[0]
        self.assertEquals(result['url'], self.image.file.url)
        
    def test_extra_links(self):
        """
        Test having multiple links works.
        """
        extra = {
            'link_headers': ['URL', 'URL Caps'],
            }
        link_content = ['Click to insert', 'Click to insert Cap']
        class CustomPicker(MockImagePicker):
            def append(self, obj):
                extra = {}
                for name in self.columns:
                    value = getattr(obj, name)
                    if isinstance(value, (datetime.datetime, datetime.date)):
                        value = value.strftime('%b %d, %Y')
                    else:
                        value = unicode(value)
                    extra[name] = value
                return {'name': unicode(obj), 'url': getattr(obj, self.field).url,
                    'extra': extra,
                    'insert': [getattr(obj, self.field).url, 
                               getattr(obj, self.field).url.upper(),],
                    'link_content': link_content,
                    }
        image_picker = CustomPicker('image_test', Image, 
                                                        None, None, extra=extra)
        response = image_picker.list(self.request)
        self.assertEquals(response.status_code, 200)
        resp = json.loads(response.content)
        self.assertEquals(resp['link_headers'], extra['link_headers'])
        self.assertEquals(resp['link_headers'], extra['link_headers'])
        result = resp['result']
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0]['insert'][0].upper(), result[0]['insert'][1])
        self.assertEquals(result[0]['link_content'], link_content)
        
    def test_search_page(self):
        """
        Make sure that the search is checking text fields and finding the 
        correct results.
        """
        for i in range(0,3):
            image = Image(
                 name = 'no find %s' % i,
                 description_1 = 'desc 1 %s' % i,
                 description_2 = 'desc 2 %s' % i,
                 file = self.image_file,
                )
            image.save()
        image_picker = MockImagePicker('image_test', Image, None, None)
        qs = image_picker.get_queryset('Test')
        images = qs.all()
        self.assertEquals(images.count(), 1)
        self.assertTrue(self.image in images)
        self.assertFalse(image in images)


class TestUploadPage(TestCase):
    """
    Test the upload 
    """
    def setUp(self):
        self.request = MockRequest()
        self.path = os.path.abspath('%s' % os.path.dirname(__file__))
        self.image_picker = MockImagePicker('image_test', Image, None, None)
        self.image_file = File(open(os.path.join(self.path, 'static/img/attach.png')), "test_file.png")

    def test_upload_form_page(self):
        """
        Test form generation.
        """
        response = self.image_picker.upload_file(self.request)
        resp = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('form' in resp)
        
    def test_upload(self):
        """
        Test the file upload and post.
        """
        request = self.request
        request.FILES = {'userfile': self.image_file,}
        response = self.image_picker.upload_file(request)
        self.assertEquals(response.status_code, 200)
        resp = json.loads(response.content)
        self.assertTrue('name' in resp)
        tmp_file = resp['name']
        request.FILES = {}
        request.POST = {
            'name': 'Test Image',
            'description_1': 'description',
            'file': tmp_file,
            }
        response = self.image_picker.upload_file(request)
        resp = json.loads(response.content)
        url = resp['url']
        images = Image.objects.all()
        self.assertEquals(images.count(), 1)
        image = images[0]
        self.assertEquals(url, image.file.url)


class TestPickerSites(TestCase):
    """
    Test the site/registration aspect of file picker.
    """
    def setUp(self):
        self.picker_name = 'test-images'
        file_picker.site.register(Image, file_picker.ImagePickerBase, name=self.picker_name,)
        self.url = reverse('filepicker:index')
        
    def test_site_index(self):
        response = self.client.get(self.url, {'pickers': [self.picker_name],})
        resp = json.loads(response.content)
        for key, value in resp['pickers'].items():
            self.assertEquals(key, self.picker_name)
            self.assertEquals(value, '/file-picker/%s/' % self.picker_name)
            
    def test_images_urls(self):
        url = reverse('filepicker:%s:init' % self.picker_name)
        response = self.client.get(self.url, {'pickers': [self.picker_name],})
        resp = json.loads(response.content)
        for key, value in resp['pickers'].items():
            response = self.client.get(value, {})
            self.assertEquals(response.status_code, 200)
