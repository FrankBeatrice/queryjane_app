$(function () {
    'use strict';

    $('.qjane-messages-link').on('click', function () {
        // Create view to load conversation bwtween company and user.
        var user_to_id = $(this).data('user-to-id');

        $.post($(this).data('load-conversation-url'), {'user_to_id': user_to_id}).done(function (response) {
            $('#messageDetailConversation').html(response.content);
        });
    });
})
