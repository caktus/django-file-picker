from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


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
        print name
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                var overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast',
                    onLoad: function() {
                        this.getOverlay().data('filePicker').load();
                    }
                }).filePicker({
                    url: '/blog/images/',
                    onImageClick: function(e, insert) {
                        this.getRoot().parent().data('wym').insert(insert);
                    }
                }).insertBefore('#id_%(name)s');
                jQuery('#id_%(name)s').wymeditor({
                    updateSelector: '.submit-row input[type=submit]',
                    updateEvent: 'click',
                    lang: '%(language)s',
                    postInit: function(wym) {
                        image_button = jQuery(wym._box).find('li.wym_tools_image a');
                        image_button.unbind();
                        image_button.click(function(e) {
                            e.preventDefault();
                            $(overlay).data('wym', wym);
                            $(overlay).data('overlay').load();
                        });
                    },
                });
            });
            </script>''' % {'name': name, 'language': self.language})
