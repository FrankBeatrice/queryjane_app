// Dependencies
import './../new_layout.js';

$(function () {
    'use strict';

    $('.EditLegalItemToggle').on('click', function() {
        $('#idEditLegalItemForm').fadeToggle("fast");
    });

    var quill_en = new Quill('#rich_editor_en_description', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_en_description').val($('#rich_editor_en_description .ql-editor').html());
    });

    var quill_es = new Quill('#rich_editor_sp_description', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_sp_description').val($('#rich_editor_sp_description .ql-editor').html());
    });

    $('#idEditLegalItemForm').validate({
        ignore: [],
        rules: {
            sp_description: {
                minlength: 40
            },
            en_description: {
                minlength: 40
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'sp_description') {
                error.insertAfter('#rich_editor_sp_description');
            } else if (element.attr('name') === 'en_description') {
                error.insertAfter('#rich_editor_en_description');
            } else {
                error.insertAfter(element);
            }
        }
    });
})
