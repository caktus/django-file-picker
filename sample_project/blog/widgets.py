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
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                var dialog = $('<div>').attr({'id':'picker-dialog', 'style':'display:none;width:200px;height:200px;z-index:999;background-color:#fff;'});
                $('body').prepend(dialog);
                $(document).data('picker', new FilePicker('/blog/images/'));
                handle_click = function(e, insert) {
                    $(document).data('wymGlob').insert(insert);
                }                
                jQuery('#id_%s').wymeditor({
                    updateSelector: '.submit-row input[type=submit]',
                    updateEvent: 'click',
                    lang: '%s',
                    postInit: function(wym) {
                        image_button = jQuery(wym._box).find('li.wym_tools_image a');
                        image_button.unbind();
                        image_button.click(function(e) {
                            jQuery(document).data('wymGlob', wym);
                            var picker = $(document).data('picker');
                            picker.show();
                            e.preventDefault();  
                            return(false);
                        });
                    },
                });
            });
            </script>''' % (name, self.language))
