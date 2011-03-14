/*
 * WYMeditor plugin for django-file-picker
 * Author: Caktus Consulting Group, LLC (http://www.caktusgroup.com/)
 * Source: https://github.com/caktus/django-file-picker
 *
 * Copyright (C) 2011 by Caktus Consulting Group, LLC
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

WYMeditor.editor.prototype.filepicker = function(options) {
    options = jQuery.extend({'rootURL': '/file-picker/'}, options);

    var wym = this,
        $element = jQuery(this._element);
        $box = jQuery(this._box);

    function install_wymeditor_file_picker(el, picker_names, urls) {
        var pickers = {};
        $.each(picker_names, function(type, name) {
            pickers[type] = urls[name];
        });
        var overlay = $('<div>').addClass('file-picker-overlay').overlay().filePicker({
            onImageClick: function(e, insert) {
                this.getRoot().parent().data('wym').insert(insert);
            }
        }).insertBefore($(el));

        if (pickers.image) {
            var image_button = $box.find('li.wym_tools_image a');
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
            var button_list = $box.find('div.wym_area_top ul');
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
    
    // extract file picker names from element and get URLs via JSON
    var picker_names = get_file_picker_types($element);
    if (picker_names) {
        var names = [];
        $.each(picker_names, function(key, val) { names.push(val); });
        $.getJSON(options['rootURL'], {'pickers': names}, function(response) {
            install_wymeditor_file_picker($element, picker_names, response.pickers);
        });
    }
};

jQuery(function() {
    $('textarea.wymeditor').each(function(idx, el) {
        $(el).wymeditor({
            updateSelector: 'input:submit',
            updateEvent: 'click',
            postInit: function(wym) {
                wym.filepicker();
            }
        });
    });
});
