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
        url_image = reverse('filepicker:blog-image:init')
        url_file = reverse('filepicker:blog-file:init')
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                var div = $('#id_%(name)s');
                div.data('conf', {'url': '%(url-file)s'});
                var file_overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast',
                    onLoad: function() {
                        this.getOverlay().data('filePicker').load();
                    }
                }).filePicker({
                    url: '%(url-file)s',
                    onImageClick: function(e, insert) {
                        this.getRoot().parent().data('wym').insert(insert);
                    }
                }).appendTo('body');
                
                var image_overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast',
                    onLoad: function() {
                        this.getOverlay().data('filePicker').load();
                    }
                }).filePicker({
                    url: '%(url-image)s',
                    onImageClick: function(e, insert) {
                        this.getRoot().parent().data('wym').insert(insert);
                    }
                }).appendTo('body');
                
                div.wymeditor({
                    updateSelector: 'input:submit',
                    updateEvent: 'click',
                    postInit: function(wym) {
                        image_button = jQuery(wym._box).find('li.wym_tools_image a');
                        image_button.unbind();
                        image_button.click(function(e) {
                            e.preventDefault();
                            $(image_overlay).data('wym', wym);
                            $(image_overlay).data('overlay').load();
                        });
                        button_list = $(wym._box).find('div.wym_area_top ul');
                        file_button = $('<a>').attr(
                            {'title': 'File', 'name': 'File', 'href':'#'}
                        ).text('File').click(function(e) {
                            e.preventDefault();
                            $(file_overlay).data('wym', wym);
                            $(file_overlay).data('overlay').load();
                        });
                        button_list.append(
                            $('<li>').addClass('wym_tools_image').append(file_button)
                        );
                    },
                });
            });
            </script>''' % {'name': name, 'language': self.language, 'url-image': url_image, 'url-file': url_file,})
            
            
