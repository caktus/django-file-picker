from django import forms
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
                        insertAtCaret('id_%(name)s', insert);
                    }
                }).appendTo('body');
                var anchor = $('<a>').text('Add Image').attr({
                    'name': 'file-picker',
                    'title': 'Add Image',
                    'href': '#'
                }).click(function(e) {
                    e.preventDefault();
                    $(overlay).data('overlay').load();
                }).prependTo('.form-row.body');
            });
            </script>''' % {'name': name})
