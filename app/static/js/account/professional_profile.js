$(function () {
    'use strict';

    // Load send message form.
    $('#id_send_message_button').on('click', function () {
        var user_to_id = $(this).data('user-to-id');
        $('#id_user_to_id').val(user_to_id);

        $('#composeMessageModal .modal-title').text("Compose message to " + $(this).data('user-to-name'));

        $.post($(this).data('load-conversation-url')).done(function (response) {
            $('#newMessageConversation').html(response.content);
        });
    });

    // Add contact to address book.
    $('#id_add_user_to_address_book').on('click', function () {
        var user_for_add_name = $(this).data('user-for-add-name');

        $.post($(this).data('add-user-to-address-book-url'), function (response) {
            if (response === 'success') {
                $('#id_add_user_to_address_book').hide();
                $('#id_remove_user_from_address_book').show();

                $.alert({
                    title: 'Well done!',
                    content: user_for_add_name + ' has been added to your address book.',
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
