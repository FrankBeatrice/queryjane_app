$(function () {
    'use strict';

    // Load send message form.
    $('#id_send_message_button').on('click', function () {
        var user_to_id = $(this).data('user-to-id');
        $('#id_user_to_id').val(user_to_id);

        $('#composeMessageModal .modal-title').text("Compose message to " + $(this).data('user-to-name'));
    });
})
