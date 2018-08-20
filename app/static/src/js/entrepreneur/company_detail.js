function score_list_update_rateyo() {
    $(".jsCompanyScoreList .jsLineScore").each(function(idx, element) {
        $(element).rateYo({
            rating: $(element).data('score'),
            readOnly: true
        });
    });
}

$(function () {
    'use strict';

    score_list_update_rateyo();

    // Load company score.
    $("#idCompanyScore").rateYo({
        rating: $('#idCompanyScore').data('score'),
        readOnly: true
    });
    
    $('#idCompanyScoreForm').on('submit', function () {
      $.post($('#idCompanyScoreForm').data('company-score-form-url'), $('#idCompanyScoreForm').serialize(), function (response) {
        $('.jsScoreFormContainer').text('Thank you. ' + response.message);
        $('#idScoreformLink').remove();
        $('.jsCompanyScoreEmpty').remove();

        $('.jsCompanyScoreList table').prepend(response.score_line);
        score_list_update_rateyo();


        $('#idScoreMessage').text(response.message);
        $("#idCompanyScore").rateYo("option", "rating", response.new_score);
      });

      return false;
    });

    // Load company score form.
    $("#idCompanyScoreInput").rateYo()
      .on("rateyo.set", function (e, data) {
          $('#id_score').val(data.rating);

      });

    $('#idCompanyScoreForm').validate({
        ignore: [],
        rules: {
            score: {
                required: true,
                maxlength: 200
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'score') {
                error.insertAfter('#idCompanyScoreInput');
            } else {
                error.insertAfter(element);
            }
        }
    });

    // Remove company score.
    $('.jsCompanyScoreList').on('click', '.jsScoreRemove', function() {
        var score_remove_url = $(this).data('company-score-remove-url');
        var score_container = $(this).closest('tr');

        $.confirm({
            title: 'Company Score',
            content: 'Do you want to remove your feedback from this company?',
            buttons: {
                remove: {
                    btnClass: 'btn-danger',
                    action: function(){
                        $.post(score_remove_url, function (response) {
                            score_container.remove();

                            $('#idScoreMessage').text(response.message);
                            $("#idCompanyScore").rateYo("option", "rating", response.new_score);
                        });
                    }
                },
                cancel: function () {}
            }
        });
    });

    // Edit company score.
    $('.jsCompanyScoreList').on('click', '.jsScoreEdit', function() {
        // Get container, score edit url and score given by current user.
        var score_container = $(this).closest('tr');
        var score_edit_url = $(this).data('company-score-edit-url');
        var score = $(this).closest('td').find('.jsLineScore').data('score');

        // Set user comment as initial value in update score form.
        $('#idCompanyScoreForm #id_comment').val($(this).closest('td').find('.jsScoreComment').data('comment'));
        // Set user score as initial value in update score form.
        $('#idCompanyScoreInput').rateYo("option", "rating", score);
        // Change submit button text.
        $('#idCompanyScoreForm button').text('Edit');
        $('.jsScoreFormContainer').show();

        // Edit company score form submit.
        $('#idCompanyScoreForm').on('submit', function () {
          $.post(score_edit_url, $('#idCompanyScoreForm').serialize(), function (response) {
            // Remove all feedback.
            score_container.remove();
            // Add new feedback.
            $('.jsCompanyScoreList table').prepend(response.score_line);
            // Remove form.
            $('.jsScoreFormContainer').text('Thank you. Your feedback has been updated');
            score_list_update_rateyo();
            $("#idCompanyScore").rateYo("option", "rating", response.new_score);
          });

          return false;
        });

    });

    // Add contact to address book.
    $('#id_add_company_to_address_book').on('click', function () {
        var company_for_add_name = $(this).data('company-for-add-name');
        var add_company_url = $(this).data('add-company-to-address-book-url');

        $.post(add_company_url, function (response) {
            if (response === 'success') {
                $('#id_add_company_to_address_book').hide();
                $('#id_remove_company_from_address_book').show();

                $.alert({
                    title: 'Well done!',
                    content: company_for_add_name + ' has been added to your address book.',
                });
            } else {
                $.alert({
                    title: 'Error!',
                    content: 'something is wrong. Please reload and try again.',
                });
            }
        });
    });

    // remove company from address book.
    $('#id_remove_company_from_address_book').on('click', function () {
        var company_for_remove_name = $(this).data('company-for-remove-name');
        var remove_company_url = $(this).data('remove-company-from-address-book-url');

        $.confirm({
            title: 'Address Book',
            content: 'Do you want to remove this company from your address book?',
            buttons: {
                remove: {
                    btnClass: 'btn-danger',
                    action: function(){
                        $.post(remove_company_url, function (response) {
                            if (response === 'success') {
                                $('#id_add_company_to_address_book').show();
                                $('#id_remove_company_from_address_book').hide();

                                $.alert({
                                    title: 'Well done!',
                                    content: company_for_remove_name + ' has been removed from your address book.',
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

    // Load send message form.
    $('#id_send_message_to_company_link').on('click', function () {
        var company_to_id = $(this).data('company-to-id');
        $('#id_company_to_id').val(company_to_id);

        $('#composeMessageModal .modal-title').text("Compose message to " + $(this).data('company-to-name'));

        $.post($(this).data('load-conversation-url')).done(function (response) {
            $('#newMessageConversation').html(response.content);
        });
    });
})
