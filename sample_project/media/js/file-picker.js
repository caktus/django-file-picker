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
        var self = this,
            tabs = null;
        
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
                tabs.tabs('div.panes > div');
                tabs.tabs().onClick(function(e, index) {
                    self.tabClick(e, index);
                });
                $.get(conf.url, function(response) {
                    conf.urls = response.urls;
                    self.getFiles();
                });
            },

            tabClick: function(e, index) {
                console.log(index);
                if (index == 1) {
                    self.getForm(); 
                }
            },
            
            getForm: function(data){
                if (!data) {
                    data = {};
                }
                $.get(conf.urls.upload.file, data, function(response){
                    self.displayForm(response);
                    self.setupUpload();
                });
            },
            
            displayForm: function(data){
                console.log(data);
                var pane = root.find('.file-picker-upload');
                pane.empty();
                pane.append($('<div>').attr('id', 'filelist'));
                var browse = $('<a>').text('Select Files').attr({
                    'href': '#',
                    'id': 'pickfiles',
                });
                pane.append(browse);
                var uploaded = $('<a>').text('Upload Files').attr({
                    'href': '#',
                    'id': 'uploadfiles',
                });
                pane.append(uploaded);
                var form = $('form').attr({'method': 'post'})
                form.html(data.form);
                form.append($('<input>').attr({'type': 'submit', 'value': 'Sumbit'}));
                pane.append(form);
            },
            
            getFiles: function(data) {
                if (!data) {
                    data = {};
                }
                $.get(conf.urls.browse.files, data, function(response) {
                    self.displayFiles(response);
                });
            },
            
            setupUpload: function() {
                var uploader = new plupload.Uploader({
                    runtimes : 'html5',//'gears,html5,flash,silverlight,browserplus',
                    browse_button : 'pickfiles',
                    max_file_size : '10mb',
                    url : conf.urls.upload.file,
                    resize : {width : 320, height : 240, quality : 90},
                    //flash_swf_url : '/media/js/plupload.flash.swf',
                    //silverlight_xap_url : '/media/js/plupload.silverlight.xap',
                    filters : [
                        {title : "Image files", extensions : "jpg,gif,png"},
                        {title : "Zip files", extensions : "zip"}
                    ]
                });
                uploader.bind('Init', function(up, params) {
                    $('#filelist').html("<div>Current runtime: " + params.runtime + "</div>");
                });
                
                uploader.bind('FilesAdded', function(up, files) {
                    $.each(files, function(i, file) {
                        $('#filelist').append(
                            '<div id="' + file.id + '">' +
                            file.name + ' (' + plupload.formatSize(file.size) + ') <b></b>' +
                        '</div>');
                    });
                });
                
                uploader.bind('UploadProgress', function(up, file) {
                    $('#' + file.id + " b").html(file.percent + "%");
                });
                
                $('#uploadfiles').click(function(e) {
                    uploader.start();
                    e.preventDefault();
                });
                uploader.init();
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
        
        // setup tabs
        var tabs = $('<ul>').addClass('css-tabs').addClass('file-picker-tabs');
        tabs.append($('<li>').append($('<a>').attr('href', '#').text('Browse')));
        tabs.append($('<li>').append($('<a>').attr('href', '#').text('Upload')));
        var panes = $('<div>').addClass('panes');
        panes.append($('<div>').attr('id', 'file-picker-browse'));
        panes.append($('<div>').addClass('file-picker-upload'));
        root.append(tabs);
        root.append(panes);
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
