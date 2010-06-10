from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


class BasicFilePickerWidget(forms.Textarea):
    def __init__(self, picker, *args, **kwargs):
        self.picker_name = picker
        super(BasicFilePickerWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        rendered = super(BasicFilePickerWidget, self).render(name, value, attrs)
        url = reverse('filepicker:%s:init' % self.picker_name)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function() {
                overlay = $('<div>').addClass('file-picker-overlay').overlay({
                    effect: 'apple',
                    speed: 'fast'
                }).filePicker({
                    url: '%(url)s',
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
            </script>''' % {'name': name, 'url': url})


class WYMeditorWidget(forms.Textarea):
    def __init__(self, pickers, *args, **kwargs):
        self.pickers = pickers
        super(WYMeditorWidget, self).__init__(*args, **kwargs)
        classes = ['wymeditor']
        if 'file' in pickers:
            classes.append("file_picker_name_file_%s" % pickers['file'])
        if 'image' in pickers:
            classes.append("file_picker_name_image_%s" % pickers['image'])
        self.attrs['class'] = ' '.join(classes)
