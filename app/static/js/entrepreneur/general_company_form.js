// Dependencies
import './../new_layout.js';

$(function () {
    'use strict';

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

    // Logo Validation
    $('#id_company_change_logo_form').validate({
        ignore: [],
        rules: {
            logo: {
                extension: 'jpg|png|jpeg',
                filesize: 4000000
            }
        },
        messages: {
            logo: {
                extension: 'Only jpg, png or jpeg files.'
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'logo') {
                error.insertAfter('#id_company_logo_update_link');
            }
        }
    });


    $('#id_company_logo_update_link').on('click', function() {
        $('#id_logo').click();
    });

    $('#id_logo').on('change', function () {
        $('#submit_company_logo_link').click();
    });

    var venture_update_logo_url = $('#id_company_change_logo_form').data('company-update-logo-url');

    $('#id_company_change_logo_form').on('submit', function() {
        var formData = new FormData(this);

        $.ajax({
            url : venture_update_logo_url,
            type: "POST",
            data : formData,
            processData: false,
            contentType: false,
            success:function(response){
                $('.jsUpdateCompanyLogoMessage').remove();
                $('.QjaneVentureSettingsLogoContainer img').attr('src', response.content);
            },
        });
        return false;
    });

    // Update venture categories
    var venture_category_url = $('.qjane-industry-categories-list').data('update-company-category-url');

    $(".qjane-industry-categories-list").on('click', '.btn', function () {
        var category_id = $(this).data('category-id');
        var new_status;
        var cat_pressed_button = $(this);

        if (cat_pressed_button.hasClass( "btn-ghost-purple" ) ) {
            // Add category
            cat_pressed_button.removeClass( "btn-ghost-purple" );
            cat_pressed_button.addClass( "btn-primary" );
            new_status = true
        } else {
            // Remove category
            cat_pressed_button.addClass( "btn-ghost-purple" );
            cat_pressed_button.removeClass( "btn-primary" );
            new_status = false
        }

        $.post(venture_category_url, {'category_id': category_id, 'new_status': new_status}, function (response) {
            if (response == 'minimum_error') {
                cat_pressed_button.addClass('btn-primary').removeClass('btn-ghost-purple');
                $('.QjaneEmptyCategoriesBug').text('You must choose at least one sector.');

                setTimeout(function(){
                     $('.QjaneEmptyCategoriesBug').text('');
                },3000);
            }
        });
    });

    // Update venture description
    $('.js_edit_desc_link').on('click', function () {
        $(this).closest('.js_lan_form_container').find('.description_field_container').show();
        $(this).closest('.js_lan_form_container').find('.desc_cont').hide();
    });


    var venture_update_description_url = $('.jsDescriptionCard').data('update-company-description-form');

    $('#id_company_change_description_form').on('submit', function() {
        if($(this).valid()) {
            var formData = new FormData(this);

            $.ajax({
                url : venture_update_description_url,
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    $('.company_description_es_content').html(response.content.description_es);
                    $('.company_description_en_content').html(response.content.description_en);

                    // Use updated_es and updated_en for hide description_field_container
                    $('.description_field_container').hide();
                    $('.js_lan_form_container').find('.desc_cont').show();

                    // Sucess message
                    if (response.content.updated_es) {
                        $('.QjaneUpdatedSPdescCompany').html('<div class="alert alert-success" role="alert">Successful update</div>');
                    }

                    if (response.content.updated_en) {
                        $('.QjaneUpdatedENdescCompany').html('<div class="alert alert-success" role="alert">Successful update</div>');
                    }
                },
            });
        }

        return false;
    });

    // Validate
    $('#id_company_change_description_form').validate({
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

    // Scroll to company settings section to activate it again.
    $("#id_activate_link_scroll").on("click", function() {
      $("html, body").animate({ scrollTop: $('#id_activate_container').offset().top }, 1000);
    });

    // Action to deactivate company on "Deactivate" click action.
    $('.jsDeactivateCompany').on('click', function() {
        var deactivate_company_url = $(this).data("deactivate-company-url");

        $.confirm({
            title: 'Do you want to deactivate this company?',
            content: 'Company profile page, and all the information related to the company will only be available for users with administrator membership for Qjane administrators.',
            buttons: {
                deactivate: {
                    btnClass: 'btn-warning',
                    action: function(){
                      $.post(deactivate_company_url, function (response) {
                          if (response === 'success') {
                            // Hide deactivate button.
                            $('#id_deactivate_container').hide();
                            // Hide activate button.
                            $('#id_activate_container').show();
                            // Hide deactivate header alert.
                            $(".jsInactiveAlert").show();

                            $.alert({
                                title: 'Deactivated!',
                                content: 'This company has been deactivated. You can activate it again when you want.',
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

    // Action to activate company on "Activate" click action.
    $('.jsActivateCompany').on('click', function() {
        $.post($(this).data("activate-company-url"), function (response) {
            if (response === 'success') {
              // Show deactivate button.
              $('#id_deactivate_container').show();
              // Hide deactivate button.
              $('#id_activate_container').hide();
              // Show deactivated company alert message.
              $(".jsInactiveAlert").hide();

              $.alert({
                  title: 'Activated!',
                  content: 'This company has been activated!!!',
              });
            } else {
              $.alert({
                  title: 'Error!',
                  content: 'something is wrong. Please reload and try again.',
              });
            }
        });
    });

  // Transfer company ownership.
  $('#id_transfer_company_ownership').on('submit', function() {
    $.confirm({
        title: 'Transfer company ownership.',
        content: 'Are you sure that you want to transfer the company ownership? New owner will have all main administration privilegies, and you will keep your role as administrator in the company.',
        buttons: {
            transfer: {
                btnClass: 'btn-warning',
                action: function(){
                  $.post($('#id_transfer_company_ownership').data('url'), $('#id_transfer_company_ownership').serialize(), function (response) {
                      if (response === 'success') {
                        $.alert({
                            title: 'Company ownership has been transfered.',
                            content: 'Transfer successfully executed.',
                        });

                        setTimeout(function () {
                          location.reload();
                        }, 1500);

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

    return false;
  });
})
