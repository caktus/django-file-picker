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
    var dialog = $('<div>').attr('id', 'picker-dialog');
    $('.form-row.body').prepend(anchor).prepend(dialog);
    $('#file-picker').data('picker', new FilePicker('/blog/images/'));
});

function FilePicker(url) {
    this.url = url;
    this.files = [];
    this.window = $('#picker-dialog');
    this.window.dialog({
        title: 'File Picker',
        width: 600,
        height: 400,
        autoOpen: false
    });
    this.show = function () {
        this.getFiles();
        this.window.dialog('open');
    }
    this.getFiles = function() {
        var picker = this;
        $.get(this.url, function(data) {
            picker.displayFiles(data.result);
        });
    }
    this.displayFiles = function(files) {
        var picker = this;
        this.window.empty();
        var table = $('<table>');
        $.each(files, function(idx, file) {
            var tr = $('<tr>');
            var img = $('<img>').attr({
                'alt': file.name,
                'src': file.thumb.url,
                'width': file.thumb.width,
                'height': file.thumb.height
            });
            tr.append($('<td>').append(img));
            tr.append($('<td>').text(file.name));
            table.append(tr);
        });
        this.window.append(table);
    }
}
