jQuery(function() {

    var FILE_PICKER_ROOT = '/file-picker/';

    // don't use square bracket syntax (jQuery 1.4.x)
    // source: http://benalman.com/news/2009/12/jquery-14-param-demystified/
    $.ajaxSetup({ traditional: true });

    function get_file_picker_types(el) {
        var picker_names = {};
        $.each($(el).attr('class').split(' '), function(idx, class_name) {
            if (class_name.substr(0, 17) == 'file_picker_name_') {
                var type = class_name.split('_')[3];
                var name = class_name.split('_')[4];
                picker_names[type] = name;
            }
        });
        return picker_names;
    }

    function install_wymeditor_file_picker(el, picker_names, urls) {
        var pickers = {};
        $.each(picker_names, function(type, name) {
            pickers[type] = urls[name];
        });
        var overlay = $('<div>').addClass('file-picker-overlay').overlay({
            effect: 'apple',
            speed: 'fast'
        }).filePicker({
            onImageClick: function(e, insert) {
                this.getRoot().parent().data('wym').insert(insert);
            }
        }).insertBefore($(el));
        $(el).wymeditor({
            updateSelector: 'input:submit',
            updateEvent: 'click',
            postInit: function(wym) {
                if (pickers.image) {
                    var image_button = jQuery(wym._box).find('li.wym_tools_image a');
                    image_button.unbind();
                    image_button.click(function(e) {
                        e.preventDefault();
                        $(overlay).data('wym', wym);
                        var conf = $(overlay).data('filePicker').getConf();
                        conf.url = pickers.image;
                        $(overlay).data('overlay').load();
                    });
                }
                if (pickers.file) {
                    var button_list = $(wym._box).find('div.wym_area_top ul');
                    var file_button = $('<a>').text('Add File').attr({
                        'title': 'File',
                        'name': 'File',
                        'href': '#'
                    }).click(function(e) {
                        e.preventDefault();
                        $(overlay).data('wym', wym);
                        var conf = $(overlay).data('filePicker').getConf();
                        conf.url = pickers.file;
                        $(overlay).data('overlay').load();
                    });
                    button_list.append(
                        $('<li>').addClass('wym_tools_file_add').append(file_button)
                    );
                }
            }
        });
    }

    $('textarea.wymeditor').each(function(idx, el) {
        var picker_names = get_file_picker_types(el);
        if (picker_names) {
            var names = [];
            $.each(picker_names, function(key, val) { names.push(val); });
            $.getJSON(FILE_PICKER_ROOT, {'pickers': names}, function(response) {
                install_wymeditor_file_picker(el, picker_names, response.pickers);
            });
        }
    });
});
