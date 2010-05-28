(function($) {

    $.filePicker = {
        conf: {
            url: '',
        }
    };

    // constructor
    function FilePicker(root, conf) {   
        
        // current instance
        var self = this;
        
        root.append($('<div>').addClass('file-picker'));
        root = root.find('.file-picker');
        
        // methods
        $.extend(self, {

            getConf: function() {
                return conf;    
            },

            getRoot: function() {
                return root;    
            },

            load: function() {
                self.getFiles();
            },

            getFiles: function(data) {
                if (!data) {
                    data = {};
                }
                $.get(conf.url, data, function(response) {
                    self.displayFiles(response);
                });
            },

            displayFiles: function(data) {
                var files = data.result;
                root.empty();
                
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
                        self.getFiles({'search': $('#search').val() });
                    })
                );
                tr.append($('<td>').append(form));
                table.append(tr);

                var tr = $('<tr>');
                tr.append($('<th>').text('Thumbnail'));
                tr.append($('<th>').text('Name'));
                table.append(tr);
                $.each(files, function(idx, file) {
                    var tr = $('<tr>');            
                    var a = $('<a>').click(function(e) {
                        $(self).trigger("onImageClick", [file.insert]);
                    });
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
                root.append(table);
                var footer = $('<div>').attr('id', 'footer');
                if (data.has_next) {
                    var next = $('<a>').attr({
                        'title': 'Next',
                        'href': '#'
                    }).text('Next').click(function(e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page + 1});
                    });
                }
                if (data.has_previous) {
                    var previous = $('<a>').attr({
                        'title': 'Next',
                        'href': '#'
                    }).text('Previous').click(function(e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page - 1});
                    });
                }
                footer.append(previous);
                footer.append(next);
                root.append(footer);
            },
        });

        // callbacks    
        $.each(['onImageClick',], function(i, name) {
            // configuration
            if ($.isFunction(conf[name])) { 
                $(self).bind(name, conf[name]); 
            }
            self[name] = function(fn) {
                $(self).bind(name, fn);
                return self;
            };
        });

    } 


    // jQuery plugin implementation
    $.fn.filePicker = function(conf) {
        // already constructed --> return API
        var el = this.data("filePicker");
        if (el) { return el; }

        conf = $.extend({}, $.filePicker.conf, conf);

        this.each(function() {
            el = new FilePicker($(this), conf);
            $(this).data("filePicker", el);
        });

        return conf.api ? el: this;
    };


})(jQuery);

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
