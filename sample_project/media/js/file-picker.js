$(document).ready(function() {
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
    $('.form-row.body').prepend(anchor);
    $('#file-picker').data('picker', new FilePicker('/blog/images/'));
});

function FilePicker(url) {
    this.url = url;
    this.files = [];
    this.show = function () {
        this.getFiles();
        
    }
    this.getFiles = function () {
        var files = [];
        $.get(this.url, function(data) {
            files = data.result;
        });
        this.files = files;
    }
}
