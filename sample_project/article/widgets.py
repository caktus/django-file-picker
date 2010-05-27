from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class FilePickerForm(forms.Textarea):
    def render(self, name, value, attrs=None):
        rendered = super(FilePickerForm, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                handle_click = function(e, insert) {
                    insertAtCaret('id_%s', insert);
                }
                var anchor = $('<a>').attr({
                    'id': 'file-picker',
                    'name': 'file-picker',
                    'href': '#'
                }).text('Add Image');
                anchor.click(function(e) {
                    e.preventDefault();
                    var picker = $(this).data('picker');
                    picker.show();
                })
                var dialog = $('<div>').attr('id', 'picker-dialog');
                $('.form-row.body').prepend(anchor).prepend(dialog);
                $('#file-picker').data('picker', new FilePicker('/article/images/'));
            });
            </script>''' % name)
