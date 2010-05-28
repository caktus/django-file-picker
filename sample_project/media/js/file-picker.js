(function($) {

    $.filePicker = {
        conf: {
            url: '',
            urls: '',
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
                self.setupTabs();
                $.get(conf.url, function(response) {
                    conf.urls = response.urls;
                    self.getFiles();
                });
            },

            getFiles: function(data) {
                if (!data) {
                    data = {};
                }
                $.get(conf.urls.browse.files, data, function(response) {
                    self.displayFiles(response);
                });
            },
            
            setupTabs: function() {
                var tabs = $('<ul>').attr('id', 'file-picker-tabs').addClass('css-tabs');
                tabs.append($('<li>').append($('<a>').attr('href', '#').text('Browse')));
                tabs.append($('<li>').append($('<a>').attr('href', '#').text('Upload')));
                var panes = $('<div>').addClass('panes');
                panes.append($('<div>').attr('id', 'file-picker-browse'));
                panes.append($('<div>').attr('id', 'file-picker-upload'));
                root.append(tabs);
                root.append(panes);
                $("ul#file-picker-tabs").tabs("div.panes > div");
            },

            displayFiles: function(data) {
                var container = root.find('#file-picker-browse');
                
                var files = data.result;
                container.empty();
                var table = $('<table>');
                var tr = $('<tr>');
                var form = $('<form>').attr({
                     'action': "",
                     'method': 'get'
                });
                form.append(
                    $('<input>').attr({ 'type': 'text', 'id':'search','name':'search'}).val(data.search)
                );
                form.append(
                    $('<input>').attr({ 'type': 'submit', 'value':'Search'}).click(
                    function(e) {
                        e.preventDefault();
                        self.getFiles({'search': $('#search').val() });
                    })
                );
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
                var div = $('<div>').attr({'class': 'scrollable'});
                container.append(form);
                container.append(div.append(table));
                var footer = $('<div>').attr('id', 'footer');
                 var next = $('<a>').attr({
                        'title': 'Next',
                        'href': '#'
                    }).text('Next')
                if (data.has_next) {
                    next.click(function(e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page + 1, 'search': $('#search').val()});
                    });
                } else {
                    next.css('color', '#bbb');
                }
                var previous = $('<a>').attr({
                        'title': 'Next',
                        'href': '#'
                    }).text('Previous ')
                if (data.has_previous) {
                    previous.click(function(e) {
                        e.preventDefault();
                        self.getFiles({'page': data.page - 1, 'search': $('#search').val()});
                    });
                } else {
                    previous.css('color', '#bbb');
                }
                footer.append(previous);
                $.each(data.pages, function(index, value){ 
                        var list = $('<a>').attr({
                            'title': value,
                            'href': '#'
                        }).text(value+' ')
                        if (data.page==value) {
                            list.css('color', '#bbb');
                        } else {
                            list.click(function(e) {
                                e.preventDefault();
                                self.getFiles({'page': value, 'search': $('#search').val()});
                            });
                        }
                        footer.append(list);
                });
                footer.append(next);
                container.append(footer);
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
