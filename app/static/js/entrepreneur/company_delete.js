$(function () {
    'use strict';

    // Validate
    $('#id_delete_company_message_form').validate({
        ignore: [],
        rules: {
            message: {
                minlength: 5,
                required: true
            }
        }
    });

    $('#id_delete_object_toggle').on('click', function() {
      $( "#id_delete_company_message_form" ).toggle();
    });

    $('#id_delete_company_message_form').on('submit', function() {
        var formData = new FormData(this);

        if($(this).valid()) {
            $.ajax({
                url : $('#id_delete_company_message_form').data('delete-company-message-form-url'),
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    if (response === 'success') {
                      $( "#id_delete_object_toggle, #id_delete_company_message_form" ).remove();
                      $.alert({
                          title: 'Thank you!',
                          content: 'Your opinion is very important for us.',
                      });
                    }
                },
            });
        }

        return false;
    });
})
