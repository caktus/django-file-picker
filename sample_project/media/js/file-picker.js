function FilePicker(url) {
    this.url = url;
    this.files = [];
    this.show = function () {
        this.getFiles();
        $('#picker-dialog').overlay({
            load: true,
            mask: {
                color: '#fff',
	        }
        });
    }
    this.getFiles = function(data) {
        if (!data) {
            data = {};
        }
        var picker = this;
        $.get(this.url, data, function(response) {
            picker.displayFiles(response);
        });
    }
    this.displayFiles = function(data) {
        var files = data.result;
        var picker = this;
        var tool = $('#picker-dialog');
        tool.empty();
        var table = $('<table>');

        var tr = $('<tr>');
        var form = $('<form>').attr({
             'action': "",
             'method': 'get'
        });
        form.append(
            $('<input>').attr({ 'type': 'text', 'id':'search','name':'search'})
        );
        form.append(
            $('<input>').attr({ 'type': 'submit', 'value':'Search'}).click(
            function(e) {
                e.preventDefault();
                picker.getFiles({'search': $('#search').val() });
            })
        );
        tr.append($('<td>').append(form));
        table.append(tr);
        
        var tr = $('<tr>');
        tr.append($('<th>').text('Thumbnail'));
        tr.append($('<th>').text('Name'));
        table.append(tr);
        $.each(files, function(idx, file) {
            var picker = this;
            var tr = $('<tr>');            
            var a = $('<a>').click(
                function(e){
                    handle_click(e, file.insert);
                }
            );
            var img = $('<img>').attr({
                'alt': file.name,
                'src': file.thumb.url,
                'width': file.thumb.width,
                'height': file.thumb.height
            });
            a.append(img);
            
            tr.append($('<td>').append(a));
            tr.append($('<td>').text(file.name));
            table.append(tr);
        });
        tool.append(table);
        var footer = $('<div>').attr('id', 'footer');
        var next = $('<a>').attr({
            'title': 'Next',
            'href': '#'
        }).text('Next').click(function(e) {
            e.preventDefault();
            picker.getFiles({'page': data.page + 1});
        });
        var previous = $('<a>').attr({
            'title': 'Next',
            'href': '#'
        }).text('Previous').click(function(e) {
            e.preventDefault();
            picker.getFiles({'page': data.page - 1});
        });
        footer.append(previous);
        footer.append(next);
        tool.append(footer);
    }
}

function insertAtCaret(areaId,text) { 
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") { txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    } else if (br == "ff") strPos = txtarea.selectionStart;
    var front = (txtarea.value).substring(0,strPos);
    var back = (txtarea.value).substring(strPos,txtarea.value.length);
    txtarea.value=front+text+back;
    strPos = strPos + text.length;
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    } else if (br == "ff") { 
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
} 
