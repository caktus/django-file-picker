
function setEditor(popup) {
    var value = popup.find('>:selected').val();
    var parent_form = popup.parents('form');
    var content_field_name = popup.attr('name').replace(/type$/, 'content');
    var content_field = parent_form.find('textarea[name=' + content_field_name + ']');
    if (value.toLowerCase() == 'wymeditor') {
        var overlay = $('<div>').addClass('file-picker-overlay').overlay({
            effect: 'apple',
            speed: 'fast'
        }).filePicker({
            url: "/file-picker/article/",
            onImageClick: function(e, insert) {
                this.getRoot().parent().data('wym').insert(insert);
            }
        }).insertBefore(content_field);
        content_field.wymeditor({
            updateSelector: 'input:submit',
            updateEvent: 'click',
            postInit: function(wym) {
                image_button = jQuery(wym._box).find('li.wym_tools_image a');
                image_button.unbind();
                image_button.click(function(e) {
                    e.preventDefault();
                    $(overlay).data('wym', wym);
                    $(overlay).data('overlay').load();
                });
            },
        });
    } else {
        jQuery.each(WYMeditor.INSTANCES, function() {
          if(this._element.attr('name') == content_field.attr('name')){
              this.update();
              $(this._box).remove();
              $(this._element).show();
              $(this._options.updateSelector).unbind(this._options.updateEvent);
              delete this;
          }
        });
        content_field.siblings('div.wym_box').remove();
        content_field.css('display', 'inline');
    }
}

jQuery(function() {
    function install_editor(popup) {
        var empty_form = $(popup).parents('div.empty-form');
        if (empty_form.length == 0) {
            setEditor($(popup));
        }
    }
    $('select[name$=type]').live('change', function() {
        install_editor($(this));
    }).each(function (i) {
        install_editor($(this));
    });
});
