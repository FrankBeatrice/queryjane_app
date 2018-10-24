import './../new_layout.js';

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

    // ---------Avatar form - init ------------- //
    // avatar Validation
    $('#id_profile_update_avatar_form').validate({
        ignore: [],
        rules: {
            avatar: {
                extension: 'jpg|png|jpeg',
                filesize: 4000000
            }
        },
        messages: {
            avatar: {
                extension: 'Only jpg, png or jpeg files.'
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'avatar') {
                error.insertAfter('#id_profile_avatar_update_link');
            }
        }
    });

    $('#id_profile_avatar_update_link').on('click', function() {
        $('#id_avatar').click();
    });

    $('#id_avatar').on('change', function () {
        $('#submit_avatar_link').click();
    });

    var update_avatar_url = $('#id_profile_update_avatar_form').data('profile-update-avatar-url');

    $('#id_profile_update_avatar_form').on('submit', function() {
        var formData = new FormData(this);

        $.ajax({
            url : update_avatar_url,
            type: "POST",
            data : formData,
            processData: false,
            contentType: false,
            success:function(response){
                $('.QjaneAccountGeneralInfo .ProfileAvatar').attr('src', response.content);
            },
        });
        return false;
    });
    // ---------Avatar form - end ------------- //


    // ---------Profile form - init ------------- //
    $('#id_user_profile_form').validate({
        ignore: [],
        rules: {
            first_name: {
                minlength: 3,
                maxlength: 50,
                required: true
            },
            last_name: {
                minlength: 3,
                maxlength: 50,
                required: true
            },
            email: {
                email: true,
                required: true
            },
        }
    });


    $('#id_user_profile_form').on('submit', function () {
        if ($(this).valid()) {
            var formData = new FormData(this);

            $.ajax({
                url : $('#id_user_profile_form').data('profile-update-url'),
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    if (response === "success") {
                        $('.successfullyProfileUpdate').show();
                    } else {
                        $('.badProfileUpdate').show();
                    }

                    setTimeout(function(){
                         $('.successfullyProfileUpdate, .badProfileUpdate').hide();
                    },3000);
                },
            });
        }

        return false;
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
            if (response != 'success') {
                alert("Please, reload and try again");
            }
        });
    });

    // Notifications
    $('.ManageEmailNotifications').on('click', '.btn', function() {
        var button = $(this);
        var notification = button.parent().data('notification');
        var value = button.data('value');

        $.post($('.ManageEmailNotifications').data('update-email-notifications-url'), {'notification': notification, 'value': value}, function (response) {
            if (response === 'success') {
                button.parent().find('.btn').removeClass('btn-primary').addClass('btn-ghost-purple');
                button.addClass('btn-primary').removeClass('btn-ghost-purple');
            }
        });
    });

    // Scroll to account settings section to activate it again.
    $("#id_activate_link_scroll").on("click", function() {
      $("html, body").animate({ scrollTop: $('#id_activate_container').offset().top }, 1000);
    });

    // Action to deactivate company on "Deactivate" click action.
    $('.jsDeactivateAccount').on('click', function() {
        var deactivate_account_url = $(this).data("deactivate-account-url");

        $.confirm({
            title: 'Do you want to deactivate your account?',
            content: 'Your pubic profile will be hidden for other users in the application. You will be able to send a receive private messages.',
            buttons: {
                deactivate: {
                    btnClass: 'btn-warning',
                    action: function(){
                      $.post(deactivate_account_url, function (response) {
                          if (response === 'success') {
                            // Hide deactivate button.
                            $('#id_deactivate_container').hide();
                            // Hide activate button.
                            $('#id_activate_container').show();
                            // Hide deactivate header alert.
                            $(".jsInactiveAlert").show();

                            $.alert({
                                title: 'Deactivated!',
                                content: 'This account has been deactivated. You can activate it again when you want.',
                            });

                          } else {
                            $.alert({
                                title: 'Error!',
                                content: 'something is wrong. Please reload and try again.',
                            });
                          }
                      });
                    }
                },
                cancel: function () {}
            }
        });
    });

    // Action to activate account on "Activate" click action.
    $('.jsActivateAccount').on('click', function() {
        $.post($(this).data("activate-account-url"), function (response) {
            if (response === 'success') {
              // Show deactivate button.
              $('#id_deactivate_container').show();
              // Hide deactivate button.
              $('#id_activate_container').hide();
              // Show deactivated company alert message.
              $(".jsInactiveAlert").hide();

              $.alert({
                  title: 'Activated!',
                  content: 'Your account has been activated!!!',
              });
            } else {
              $.alert({
                  title: 'Error!',
                  content: 'something is wrong. Please reload and try again.',
              });
            }
        });
    });
})
