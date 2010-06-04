from django.db.models.base import ModelBase

import file_picker


class FilePickerSite(object):

    def __init__(self, name=None, app_name='file-picker'):
        self._registry = []

    def register(self, model_or_iterable, class_=None, name=None, **options):
        if not class_:
            class_ = file_picker.FilePickerBase
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if not name:
                view_name = class_.__class__.__name__.lower()
                model_name = model().__class__.__name__.lower()
                name = "%s-%s" % (model_name, view_name)
            self._registry.append({'name': name, 'picker': class_(model)})

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include
        urlpatterns = patterns('', url(r'^$', self.primary))
        for p in self._registry:
            urlpatterns += url(r'^%s/' % p['name'], include(p['picker'].urls)),
        return urlpatterns
    urls = property(get_urls)

    def primary(self, request):
        pass

site = FilePickerSite()
