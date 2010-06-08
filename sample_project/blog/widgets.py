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
                overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast'
                }).filePicker({
                    onImageClick: function(e, insert) {
                        this.getRoot().parent().data('wym').insert(insert);
                    }
                }).appendTo('body');

                var div = $('#id_%(name)s');                
                div.wymeditor({
                    updateSelector: 'input:submit',
                    updateEvent: 'click',
                    postInit: function(wym) {
                        image_button = jQuery(wym._box).find('li.wym_tools_image a');
                        image_button.unbind();
                        image_button.click(function(e) {
                            e.preventDefault();
                            $(overlay).data('wym', wym);
                            conf = $(overlay).data('filePicker').getConf();
                            conf.url = '%(url-image)s';
                            $(overlay).data('overlay').load();
                        });
                        button_list = $(wym._box).find('div.wym_area_top ul');
                        file_button = $('<a>').attr({
                            'title': 'File', 'name': 'File', 'href':'#'
                        }).css({
                            'background': 
                            'transparent url(%(MEDIA_URL)s/img/attach.png) no-repeat center center'
                        }).text('Add File').click(function(e) {
                            e.preventDefault();
                            $(overlay).data('wym', wym);
                            conf = $(overlay).data('filePicker').getConf();
                            conf.url = '%(url-file)s';
                            $(overlay).data('overlay').load();
                        });
                        button_list.append(
                            $('<li>').addClass('wym_tools_file_add').append(file_button)
                        );
                    }
                });
            });
            </script>''' % {
                'name': name, 'language': self.language, 
                'url-image': url_image, 'url-file': url_file,
                'MEDIA_URL': settings.MEDIA_URL
            })
            
            
