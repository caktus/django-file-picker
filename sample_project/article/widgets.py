from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class FilePickerForm(forms.Textarea):
    def render(self, name, value, attrs=None):
        rendered = super(FilePickerForm, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                var overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast',
                    onLoad: function() {
                        this.getOverlay().data('filePicker').load();
                    }
                }).filePicker({
                    url: '/article/images/',
                    onImageClick: function(e, insert) {
                        insertAtCaret('id_%s', insert);
                    }
                }).appendTo($('body'));
                var anchor = $('<a>').attr({
                    'id': 'file-picker',
                    'name': 'file-picker',
                    'href': '#'
                }).text('Add Image');
                anchor.click(function(e) {
                    e.preventDefault();
                    $(overlay).data('overlay').load();
                })
                $('.form-row.body').prepend(anchor);
            });
            </script>''' % name)
