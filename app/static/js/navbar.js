$(function () {
  'use strict';
    // Populate general message modal with new notification detail.
    $('.header-notification-list, .QjaneNotificationsList').on('click', '.qjane-notification-link', function () {
        var notification_url = $(this).data('notification-url');

        // Remove active class
        $(this).closest('tr').removeClass("active");
        $(this).parent().find('.JSNotificationStatus').removeClass('fa-eye-slash').addClass('fa-eye');

        $.post(notification_url).done(function (response) {
            if (response != 'fail') {
                $('#generalModalMessage .modal-content').html(response.content);
                $('.NewNotificationsCounter').text(response.new_notifications_counter);
            } else {
              alert('something is wrong. Please reload and try again.');
            }
        });
    });

    // Load send message form.
    $('.JSComposeMessage').on('click', function () {
        var user_to_id = $(this).data('user-to-id');
        var company_to_id = $(this).data('company-to-id');
        var company_from_id = $(this).data('company-from-id');
        var load_conversation_url = $(this).data('load-conversation-url');

        if (user_to_id != undefined) {
          $('#id_user_to_id').val(user_to_id);
        }

        if (company_to_id != undefined) {
          $('#id_company_to_id').val(company_to_id);
        }

        if (company_from_id != undefined) {
          $('#id_company_from_id').val(company_from_id);
        }

        $('#composeMessageModal .modal-title').text("Compose message to " + $(this).data('to-name'));


        if (load_conversation_url){
          $.post($(this).data('load-conversation-url')).done(function (response) {
              $('#JSconversationDetail').html(response.content);

                $('#generalModalMessage .modal-content').html(response.content);
                $('.NewMessagesCounter').text(response.new_messages_counter);
          });
        }
    });

    $('#composeMessageModal').on('hidden.bs.modal', function() {
      $('#composeMessageModal .modal-body .alert-success').hide();
      $('#composeMessageModal #id_send_message_form').show();
      $('#id_user_message, #id_user_to_id').val("");
    })

    // Submit message form
    $('#id_send_message_form').on('submit', function() {
      $.post($(this).data('send-message-url'), $('#id_send_message_form').serialize(), function (response) {
          if (response === 'success') {
            $('#composeMessageModal .modal-body .alert-success').show();
            $('#composeMessageModal #id_send_message_form').hide();
          }
      });

      return false;
    });
})
