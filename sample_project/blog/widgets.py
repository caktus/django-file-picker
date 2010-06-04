from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


class WYMEditor(forms.Textarea):
    class Media:
        js = (
            'wymeditor/jquery.wymeditor.pack.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(WYMEditor, self).render(name, value, attrs)
        url = reverse('')#reverse("file-picker-blog-image-init");
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                var div = $('#id_%(name)s');
                div.data('conf', {'url': '%(url)s'});
            });
            </script>''' % {'name': name, 'language': self.language, 'url': url})
