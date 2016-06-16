/*jshint strict:true, browser:true, jquery:true */
(function($) {
    'use strict';

    $(function () {
        var textarea = $('#id_content');
        var editDiv = $('<div>', {
            position: 'absolute',
            width: textarea.width(),
            height: textarea.height(),
            'class': textarea.attr('class')
        }).insertBefore(textarea);
        textarea.css('visibility', 'hidden');
        var editor = ace.edit(editDiv[0]);
        editor.renderer.setShowGutter(false);
        editor.getSession().setValue(textarea.val());
        editor.getSession().setMode('ace/mode/markdown');
        editor.getSession().setUseWrapMode(true);

        editor.setTheme('ace/theme/chrome');
        editor.setHighlightActiveLine(false);
        editor.setShowPrintMargin(false);

        // copy back to textarea on form submit...
        textarea.closest('form').submit(function () {
            textarea.val(editor.getSession().getValue());
        });
    });
})(django.jQuery);
