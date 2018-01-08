$(function () {
    'use strict';

    $('.QjaneShareGPSfigure, .QjaneShareGPStext').on('click', function() {
        getLocation();
    });

    var quill_en = new Quill('#rich_editor_description_en', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_description_en').val($('#rich_editor_description_en .ql-editor').html());
    });

    var quill_es = new Quill('#rich_editor_description_es', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_description_es').val($('#rich_editor_description_es .ql-editor').html());
    });

    // Update venture description
    $('.js_edit_desc_link').on('click', function () {
        $(this).closest('.js_lan_form_container').find('.description_field_container').show();
        $(this).closest('.js_lan_form_container').find('.desc_cont').hide();
    });

    var profile_update_description_url = $('.QjaneProfileUpdateDescriptionContainer').data('update-profile-description-form');

    $('#id_profile_change_description_form').on('submit', function() {
        if($(this).valid()) {
            var formData = new FormData(this);

            $.ajax({
                url : profile_update_description_url,
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    $('.profile_description_es_content').html(response.content.description_es);
                    $('.profile_description_en_content').html(response.content.description_en);

                    // Use updated_es and updated_en for hide description_field_container
                    $('.description_field_container').hide();
                    $('.js_lan_form_container').find('.desc_cont').show();

                    // Sucess message
                    if (response.content.updated_es) {
                        $('.QjaneUpdatedSPdescProfile').html('<div class="alert alert-success" role="alert">Successful update</div>');
                    }

                    if (response.content.updated_en) {
                        $('.QjaneUpdatedENdescProfile').html('<div class="alert alert-success" role="alert">Successful update</div>');
                    }
                },
            });
        }

        return false;
    });

    // Validate
    $('#id_profile_change_description_form').validate({
        ignore: [],
        rules: {
            description_en: {
                minlength: 40
            },
            description_es: {
                minlength: 40
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'description_es') {
                error.insertAfter('#rich_editor_description_es');
            } else if (element.attr('name') === 'description_en') {
                error.insertAfter('#rich_editor_description_en');
            } else {
                error.insertAfter(element);
            }
        }
    });

    // Update professional profile category
    var pp_category_url = $('.qjane-industry-categories-list').data('update-professional-profile-category-url');

    $(".qjane-industry-categories-list").on('click', '.btn', function () {
        var category_id = $(this).data('category-id');
        var new_status;

        if ( $( this ).hasClass( "btn-ghost-purple" ) ) {
            // Add category
            $( this ).removeClass( "btn-ghost-purple" );
            $( this ).addClass( "btn-primary" );
            new_status = true
        } else {
            // Remove category
            $( this ).addClass( "btn-ghost-purple" );
            $( this ).removeClass( "btn-primary" );
            new_status = false
        }

        $.post(pp_category_url, {'category_id': category_id, 'new_status': new_status}, function (response) {
            console.log("response");
        });
    });
})
